import os
import sys
import shutil
import re
import datetime
import logging
from pathlib import Path
try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Error: Pillow or pytesseract not installed. Please install them.")
    sys.exit(1)

# --- Configuration ---
WATCH_DIR = Path(r"C:\Users\hirak\Desktop")
# Target markdown file
DIET_MD_PATH = Path(r"C:\Users\hirak\Desktop\2nd-Brain\01_ダイエット\記録.md")
# Where to move processed screenshots
ASSETS_DIR = Path(r"C:\Users\hirak\Desktop\2nd-Brain\01_ダイエット\assets\screenshots")
LOG_FILE = Path(__file__).parent / "auto_diet.log"

# Tesseract Configuration
# If tesseract is not in PATH, specify it here:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


def format_md_date(value: datetime.date) -> str:
    """Return M/D format in a Windows-compatible way."""
    return f"{value.month}/{value.day}"

def send_notification(title, message):
    """Sends a Windows Toast notification using PowerShell."""
    try:
        ps_command = f"""
        New-BurntToastNotification -Text "{title}", "{message}"
        """
        import subprocess
        subprocess.run(["powershell", "-c", ps_command], capture_output=True)
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")

def extract_data_from_image(image_path):
    """
    Extracts weight, body fat, etc. from the image using OCR.
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGB") # Convert to RGB to handle MPO or other formats
        # Use Japanese and English
        text = pytesseract.image_to_string(img, lang='jpn+eng')
        
        logging.info(f"OCR Result for {image_path}:\n{text}")

        data = {}
        
        # Keywords to identify if this is a diet screenshot
        keywords = ["体重", "体脂肪", "BMI", "kg", "内臓脂肪", "骨格筋", "最高", "最低", "血圧"]
        hit_count = sum(1 for k in keywords if k in text)
        
        if hit_count < 2:
            logging.info("Not enough keywords found. Probably not a diet screenshot.")
            return None

        # --- Parsing Logic (Heuristic) ---
        # 1. Weight (XX.X kg)
        # Look for pattern like "94.0 kg" or "94.0kg" or just "94.0" near "体重"
        weight_match = re.search(r'(\d{2,3}[\.,]\d)[\s]*k?g?', text, re.IGNORECASE)
        if weight_match:
            data['weight'] = float(weight_match.group(1).replace(',', '.'))

        # 2. Body Fat (XX.X %)
        # Look for pattern near "体脂肪"
        fat_match = re.search(r'体脂肪.*?(\d{1,2}[\.,]\d)', text, re.DOTALL)
        if fat_match:
            data['fat'] = float(fat_match.group(1).replace(',', '.'))
            
        # 3. Date
        # Try to find a date like 2/14 or 2026/02/14
        date_match = re.search(r'(202\d)[/\.](\d{1,2})[/\.](\d{1,2})', text)
        if date_match:
            data['date'] = datetime.date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        else:
             short_date_match = re.search(r'(\d{1,2})[/\.](\d{1,2})', text)
             if short_date_match:
                 # Assume current year
                 current_year = datetime.date.today().year
                 data['date'] = datetime.date(current_year, int(short_date_match.group(1)), int(short_date_match.group(2)))
             else:
                 data['date'] = datetime.date.today()

        # 4. Blood Pressure (SYS/DIA)
        # Look for pattern like "150/96" or "120 / 80"
        # Also support finding distinct numbers if they are labeled "最高" "最低"
        bp_match = re.search(r'(\d{2,3})[\s/]+(\d{2,3})', text)
        if bp_match:
            # Basic validation: SYS should be higher than DIA, usually SYS > 80, DIA > 40
            sys_val = int(bp_match.group(1))
            dia_val = int(bp_match.group(2))
            if sys_val > dia_val and sys_val > 50:
                data['bp'] = f"{sys_val}/{dia_val}"
        
        return data

    except Exception as e:
        logging.error(f"OCR Failed: {e}")
        return None

def update_markdown(data):
    """
    Updates the diet markdown file with the extracted data.
    """
    if not DIET_MD_PATH.exists():
        logging.error(f"Markdown file not found: {DIET_MD_PATH}")
        return False

    try:
        content = DIET_MD_PATH.read_text(encoding='utf-8')
        
        date_str = format_md_date(data['date'])  # e.g., 2/14
        weight = data.get('weight')
        fat = data.get('fat')
        bp = data.get('bp', '-')
        
        if not weight:
            logging.warning("No weight data found, skipping markdown update.")
            return False

        # --- 1. Update Weekly Trend Table ---
        # Check if entry already exists
        # Update regex to handle the new BP column
        row_pattern = re.compile(rf"\|\s*{re.escape(date_str)}\s*\|\s*{weight}kg\s*\|", re.IGNORECASE)
        if row_pattern.search(content):
            logging.info("Entry already exists in table.")
            # TODO: Ideally update the existing row if BP data is new, but for now skip simple duplicate
        else:
            # Insert at top of the table (after the header separator)
            # Find the header separator position
            header_sep_match = re.search(r'\|\s*:---\s*\|\s*:---\s*\|\s*:---\s*\|\s*:---\s*\|\n', content)
            if header_sep_match:
                insert_pos = header_sep_match.end()
                new_row = f"| {date_str} | {weight}kg | - | {bp} |\n"
                content = content[:insert_pos] + new_row + content[insert_pos:]
                logging.info(f"Inserted new row for {date_str} into Weekly Trend.")

        # --- 2. Update Daily Summary (If today) ---
        if data['date'] == datetime.date.today():
             # Replac current weight in header
             # > **最新体重**: 93.1kg
             content = re.sub(r'(\*\*最新体重\*\*: )[\d\.]+kg', fr'\g<1>{weight}kg', content)
             
             # Update date in header
             # ## 🧘‍♂️ 今日の振り返り (2/14)
             content = re.sub(r'(## 🧘‍♂️ 今日の振り返り \()[\d/]+\)', fr'\g<1>{date_str})', content)
             
             logging.info("Updated daily summary header.")

        # --- 3. Update Timeline ---
        # Check if timeline entry exists
        timeline_header = f"### {date_str}"
        if timeline_header not in content:
            # Create new timeline entry
            weekday_ja = ["月", "火", "水", "木", "金", "土", "日"][data['date'].weekday()]
            new_timeline = f"""
### {date_str} ({weekday_ja}) — {weight}kg

| 指標 | 値 | 指標 | 値 |
| :--- | :--- | :--- | :--- |
| 体脂肪 | {fat}% | 皮下脂肪 | - |
| 骨格筋 | - | 内臓脂肪 | - |
| 代謝 | - | 体内年齢 | - |
| BMI | - | 血圧 | {bp} |
| ウエスト | - | - | - |

> **メモ**: (自動取得)

---
"""
            # Insert after "## 🗓️ タイムライン"
            insert_marker = "## 🗓️ タイムライン"
            if insert_marker in content:
                 content = content.replace(insert_marker, f"{insert_marker}\n{new_timeline}")
                 logging.info(f"Added timeline entry for {date_str}.")

        DIET_MD_PATH.write_text(content, encoding='utf-8')
        return True

    except Exception as e:
        logging.error(f"Failed to update markdown: {e}")
        return False

def move_screenshot(src_path):
    """Moves the processed screenshot to the assets folder."""
    try:
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        filename = src_path.name
        dst_path = ASSETS_DIR / filename
        
        # Handle duplicate filenames
        if dst_path.exists():
            timestamp = datetime.datetime.now().strftime("%H%M%S")
            dst_path = ASSETS_DIR / f"{src_path.stem}_{timestamp}{src_path.suffix}"
            
        shutil.move(str(src_path), str(dst_path))
        logging.info(f"Moved screenshot to: {dst_path}")
        return dst_path
    except Exception as e:
        logging.error(f"Failed to move file: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_diet_screenshot.py <image_path>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        logging.error(f"File not found: {image_path}")
        sys.exit(1)

    logging.info(f"Processing: {image_path}")

    # 1. Extract Data
    data = extract_data_from_image(image_path)
    if not data:
        logging.info("No diet data found. Exiting.")
        sys.exit(0)

    # 2. Update Markdown
    if update_markdown(data):
        msg = f"Recorded: {data.get('weight')}kg"
        if data.get('bp'):
            msg += f", BP: {data.get('bp')}"
        send_notification("Diet Update Success", msg)
        
        # 3. Move File
        moved_path = move_screenshot(image_path)
        if moved_path:
             logging.info("All done.")
    else:
        logging.warning("Markdown update failed or was skipped.")

if __name__ == "__main__":
    main()
