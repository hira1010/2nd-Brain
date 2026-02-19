import argparse
import datetime
import logging
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib import config
from lib.utils import setup_logger

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Error: Pillow or pytesseract not installed. Please install them.")
    raise SystemExit(1)


DEFAULT_DIET_MD_PATH = config.DIET_DIR / "記録.md"
DEFAULT_ASSETS_DIR = config.DIET_DIR / "assets" / "screenshots"
DEFAULT_LOG_FILE = Path(__file__).parent / "auto_diet.log"
DEFAULT_TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

TIMELINE_SECTION_MARKER = "## 欄・・繧ｿ繧､繝繝ｩ繧､繝ｳ"

logger = setup_logger("scripts.auto_diet_screenshot")


@dataclass
class DietData:
    weight: Optional[float] = None
    fat: Optional[float] = None
    date: Optional[datetime.date] = None
    bp: Optional[str] = None


def configure_logging(log_file: Path) -> None:
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if not any(isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "") == str(log_file.resolve()) for h in root.handlers):
        root.addHandler(file_handler)


def configure_tesseract(binary_path: Optional[Path]) -> None:
    candidate = binary_path or DEFAULT_TESSERACT_PATH
    if candidate.exists():
        pytesseract.pytesseract.tesseract_cmd = str(candidate)


def format_md_date(value: datetime.date) -> str:
    return f"{value.month}/{value.day}"


def send_notification(title: str, message: str) -> None:
    try:
        ps_command = f'New-BurntToastNotification -Text "{title}", "{message}"'
        subprocess.run(["powershell", "-c", ps_command], capture_output=True, check=False)
    except Exception as exc:
        logger.error("Failed to send notification: %s", exc)


def is_diet_like_text(text: str) -> bool:
    keywords = [
        "kg",
        "BMI",
        "体重",
        "体脂肪",
        "血圧",
        "内臓脂肪",
        "菴馴㍾",
        "菴楢р閧ｪ",
        "鬪ｨ譬ｼ遲",
    ]
    hits = sum(1 for word in keywords if word in text)
    return hits >= 2


def parse_date(text: str) -> datetime.date:
    full_date = re.search(r"(202\d)[/\.](\d{1,2})[/\.](\d{1,2})", text)
    if full_date:
        return datetime.date(int(full_date.group(1)), int(full_date.group(2)), int(full_date.group(3)))

    short_date = re.search(r"(\d{1,2})[/\.](\d{1,2})", text)
    if short_date:
        year = datetime.date.today().year
        return datetime.date(year, int(short_date.group(1)), int(short_date.group(2)))

    return datetime.date.today()


def parse_weight(text: str) -> Optional[float]:
    match = re.search(r"(\d{2,3}[\.,]\d)[\s]*k?g?", text, re.IGNORECASE)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def parse_fat(text: str) -> Optional[float]:
    fat_match = re.search(r"(?:体脂肪|菴楢р閧ｪ).*?(\d{1,2}[\.,]\d)", text, re.DOTALL)
    if not fat_match:
        return None
    return float(fat_match.group(1).replace(",", "."))


def parse_blood_pressure(text: str) -> Optional[str]:
    match = re.search(r"(\d{2,3})[\s/]+(\d{2,3})", text)
    if not match:
        return None

    sys_val = int(match.group(1))
    dia_val = int(match.group(2))
    if 50 < sys_val <= 260 and 30 < dia_val <= 200 and sys_val > dia_val:
        return f"{sys_val}/{dia_val}"
    return None


def extract_data_from_image(image_path: Path) -> Optional[DietData]:
    try:
        image = Image.open(image_path).convert("RGB")
        text = pytesseract.image_to_string(image, lang="jpn+eng")
        logger.info("OCR result for %s:\n%s", image_path, text)

        if not is_diet_like_text(text):
            logger.info("Not enough diet keywords found. Skip file: %s", image_path)
            return None

        data = DietData(
            weight=parse_weight(text),
            fat=parse_fat(text),
            date=parse_date(text),
            bp=parse_blood_pressure(text),
        )
        return data
    except Exception as exc:
        logger.error("OCR failed: %s", exc)
        return None


def insert_weekly_row(content: str, date_str: str, weight: float, bp: str) -> str:
    row_pattern = re.compile(rf"\|\s*{re.escape(date_str)}\s*\|\s*{weight}kg\s*\|", re.IGNORECASE)
    if row_pattern.search(content):
        logger.info("Weekly row already exists for %s", date_str)
        return content

    header_sep_match = re.search(r"\|\s*:---\s*\|\s*:---\s*\|\s*:---\s*\|\s*:---\s*\|\n", content)
    if not header_sep_match:
        logger.warning("Weekly table header not found")
        return content

    new_row = f"| {date_str} | {weight}kg | - | {bp} |\n"
    return content[: header_sep_match.end()] + new_row + content[header_sep_match.end() :]


def update_daily_header_if_today(content: str, date_value: datetime.date, date_str: str, weight: float) -> str:
    if date_value != datetime.date.today():
        return content

    updated = re.sub(r"(\*\*譛譁ｰ菴馴㍾\*\*: )[\d\.]+kg", fr"\g<1>{weight}kg", content)
    updated = re.sub(r"(## .*\()[\d/]+\)", fr"\g<1>{date_str})", updated, count=1)
    return updated


def build_timeline_block(date_value: datetime.date, date_str: str, weight: float, fat: Optional[float], bp: str) -> str:
    weekday_ja = ["月", "火", "水", "木", "金", "土", "日"][date_value.weekday()]
    fat_text = f"{fat}%" if fat is not None else "-"

    return f"""
### {date_str} ({weekday_ja}) · {weight}kg

| 項目 | 値 | 項目 | 値 |
| :--- | :--- | :--- | :--- |
| 体脂肪 | {fat_text} | 内臓脂肪 | - |
| 筋肉率 | - | 基礎代謝 | - |
| 摂取量 | - | 体内年齢 | - |
| BMI | - | 血圧 | {bp} |
| ウエスト | - | - | - |

> **メモ**: (自動追記)

---
"""


def insert_timeline_entry(content: str, data: DietData) -> str:
    assert data.date is not None
    assert data.weight is not None

    date_str = format_md_date(data.date)
    timeline_header = f"### {date_str}"
    if timeline_header in content:
        logger.info("Timeline already exists for %s", date_str)
        return content

    new_block = build_timeline_block(
        date_value=data.date,
        date_str=date_str,
        weight=data.weight,
        fat=data.fat,
        bp=data.bp or "-",
    )

    if TIMELINE_SECTION_MARKER in content:
        return content.replace(TIMELINE_SECTION_MARKER, f"{TIMELINE_SECTION_MARKER}\n{new_block}", 1)

    logger.warning("Timeline section marker not found. Appending at end.")
    return f"{content}\n{new_block}"


def update_markdown(data: DietData, markdown_path: Path) -> bool:
    if not markdown_path.exists():
        logger.error("Markdown file not found: %s", markdown_path)
        return False

    if data.weight is None or data.date is None:
        logger.warning("Weight/date not found in OCR result. Skip markdown update.")
        return False

    try:
        content = markdown_path.read_text(encoding="utf-8")
        date_str = format_md_date(data.date)

        content = insert_weekly_row(content, date_str=date_str, weight=data.weight, bp=data.bp or "-")
        content = update_daily_header_if_today(content, date_value=data.date, date_str=date_str, weight=data.weight)
        content = insert_timeline_entry(content, data)

        markdown_path.write_text(content, encoding="utf-8")
        return True
    except Exception as exc:
        logger.error("Failed to update markdown: %s", exc)
        return False


def move_screenshot(src_path: Path, assets_dir: Path) -> Optional[Path]:
    try:
        assets_dir.mkdir(parents=True, exist_ok=True)
        dst_path = assets_dir / src_path.name

        if dst_path.exists():
            timestamp = datetime.datetime.now().strftime("%H%M%S")
            dst_path = assets_dir / f"{src_path.stem}_{timestamp}{src_path.suffix}"

        shutil.move(str(src_path), str(dst_path))
        logger.info("Moved screenshot to: %s", dst_path)
        return dst_path
    except Exception as exc:
        logger.error("Failed to move file: %s", exc)
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OCR a diet screenshot and update markdown.")
    parser.add_argument("image_path", type=Path, help="Input screenshot path")
    parser.add_argument("--diet-md", type=Path, default=DEFAULT_DIET_MD_PATH)
    parser.add_argument("--assets-dir", type=Path, default=DEFAULT_ASSETS_DIR)
    parser.add_argument("--log-file", type=Path, default=DEFAULT_LOG_FILE)
    parser.add_argument("--tesseract", type=Path, default=DEFAULT_TESSERACT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_logging(args.log_file)
    configure_tesseract(args.tesseract)

    image_path = args.image_path
    if not image_path.exists():
        logger.error("File not found: %s", image_path)
        return 1

    logger.info("Processing: %s", image_path)

    data = extract_data_from_image(image_path)
    if not data:
        logger.info("No diet data found. Exiting.")
        return 0

    if update_markdown(data, markdown_path=args.diet_md):
        message = f"Recorded: {data.weight}kg"
        if data.bp:
            message += f", BP: {data.bp}"
        send_notification("Diet Update Success", message)

        moved_path = move_screenshot(image_path, assets_dir=args.assets_dir)
        if moved_path:
            logger.info("All done")
    else:
        logger.warning("Markdown update failed or skipped")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
