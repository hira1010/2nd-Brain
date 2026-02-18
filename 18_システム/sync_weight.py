#!/usr/bin/env python3
"""
体重データ同期＆振り返り統合スクリプト。
Googleスプレッドシートから最新の体重を取得し、Markdownを更新します。
"""

import os
import re
import statistics
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd

# プロジェクトルートをパスに追加（libのインポート用）
LIB_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LIB_PARENT not in sys.path:
    sys.path.append(LIB_PARENT)

from lib import config, sheets, utils

SHEET_ID = config.DIET_SHEET_ID
GID = "0"
TARGET_MD = config.DIET_DIR / "記録.md"
TARGET_YEAR = 2026
WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
TIMELINE_MARKER = "## 🗓️ タイムライン"

HEADER_RE = re.compile(
    r"^###\s+(\d{1,2})/(\d{1,2})\s+\([^)]+\)\s+[—─-]+\s+(?:\*\*)?([0-9.]+)(?:\*\*)?kg",
    re.MULTILINE,
)
BODY_FAT_RE = re.compile(r"体脂肪:\s*([0-9.]+)%")
VISCERAL_FAT_RE = re.compile(r"内臓脂肪:\s*([0-9.]+)")

logger = utils.setup_logger("sync_weight")


@dataclass(frozen=True)
class WeightRecord:
    """体重記録の保持用モデル。"""

    date: str
    weight: float
    waist: Optional[float] = None
    body_fat: Optional[float] = None
    visceral_fat: Optional[float] = None

    @property
    def sort_key(self) -> Tuple[int, int]:
        month, day = self.date.split("/")
        return int(month), int(day)


def normalize_date(date_text: str) -> str:
    """日付テキストの '01/01' 形式を '1/1' に正規化します。"""
    raw = str(date_text).strip()
    match = re.match(r"^\s*(\d{1,2})/(\d{1,2})\s*$", raw)
    if not match:
        return re.sub(r"/0", "/", raw)
    month = int(match.group(1))
    day = int(match.group(2))
    return f"{month}/{day}"


def format_header(date_text: str, weight_text: str) -> str:
    """タイムライン用ヘッダーを作成します。"""
    normalized = normalize_date(date_text)
    try:
        dt = datetime.strptime(f"{TARGET_YEAR}/{normalized}", "%Y/%m/%d")
        weekday = WEEKDAYS[dt.weekday()]
        return f"### {dt.month}/{dt.day} ({weekday}) ── {weight_text}kg"
    except ValueError:
        return f"### {normalized} ── {weight_text}kg"


def entry_exists(content: str, date_text: str) -> bool:
    """同一日付の見出しがすでに存在するかを判定します。"""
    normalized = normalize_date(date_text)
    escaped = re.escape(normalized)
    return re.search(rf"^###\s+{escaped}\s+\([^)]+\)", content, re.MULTILINE) is not None


def parse_existing_records(content: str) -> List[WeightRecord]:
    """Markdown本文から既存の体重記録を抽出します。"""
    records: List[WeightRecord] = []

    for match in HEADER_RE.finditer(content):
        month = int(match.group(1))
        day = int(match.group(2))
        weight = float(match.group(3))
        date_str = f"{month}/{day}"

        section_start = match.end()
        next_match = HEADER_RE.search(content, section_start)
        section_end = next_match.start() if next_match else len(content)
        section = content[section_start:section_end]

        body_fat = None
        visceral_fat = None
        bf_match = BODY_FAT_RE.search(section)
        if bf_match:
            body_fat = float(bf_match.group(1))
        vf_match = VISCERAL_FAT_RE.search(section)
        if vf_match:
            visceral_fat = float(vf_match.group(1))

        records.append(WeightRecord(date_str, weight, None, body_fat, visceral_fat))

    return sorted(records, key=lambda r: r.sort_key, reverse=True)


def generate_advice(records: List[WeightRecord]) -> str:
    """最新データに基づいたアドバイス文を生成します。"""
    if len(records) < 2:
        return "データが不足しています。継続して記録しましょう。"

    latest = records[0]
    previous = records[1]
    diff = latest.weight - previous.weight
    week_avg = statistics.mean([r.weight for r in records[:7]])

    advice_lines = [
        "## 🎯 今日の振り返りとアドバイス\n",
        f"**日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n",
        "### 📊 体重推移の分析\n",
        f"- **最新体重**: {latest.weight}kg",
    ]

    if diff < 0:
        advice_lines.append(f"- **前回比**: {abs(diff):.1f}kg 減 ✨ 素晴らしい！")
        advice_lines.append("- 💪 **Good Job!** 身体が本来の機能を取り戻しつつあります！")
    elif diff > 0:
        advice_lines.append(f"- **前回比**: +{diff:.1f}kg")
        advice_lines.append("- 🌱 **大丈夫!** 体重は波があるもの。長期的なトレンドを見ましょう。")
    else:
        advice_lines.append("- **前回比**: 変化なし（安定）")

    advice_lines.append(f"- **週間平均**: {week_avg:.1f}kg")
    advice_lines.append("\n### 🧘‍♂️ 今日のアクションプラン\n")
    advice_lines.append("> 「失われた身体機能を呼び戻す」 - Ninniki-nene Style\n")

    if diff >= 0.5:
        advice_lines.append("- ✅ 16時間断食を再確認")
        advice_lines.append("- ✅ スワイショウ（腕振り運動）で代謝の向上")
    else:
        advice_lines.append("- ✅ 現在のリズムをキープ！")
        advice_lines.append("- ✅ 座りながらドローイン（腹圧を意識）")

    advice_lines.append('\n**📝 今日の一言**: "一喜一憂せず、本来の自分の身体機能を取り戻しましょう！"')
    return "\n".join(advice_lines)


def to_cell_text(value: object) -> str:
    """セル値をMarkdown向けの表示文字列に変換します。"""
    if pd.isna(value):
        return "-"
    return str(value).strip()


def with_percent(value: str) -> str:
    """値が存在する場合だけパーセント表記を付与します。"""
    return f"{value}%" if value != "-" else "-"


def cell_at(row: pd.Series, index: int) -> str:
    """行の指定列を安全に取得します。"""
    if index >= len(row):
        return "-"
    return to_cell_text(row.iloc[index])


def extract_latest_measurement(df: pd.DataFrame) -> Optional[Tuple[str, str, Dict[str, str]]]:
    """スプレッドシートから最新1行の体重データを抽出します。"""
    valid_data = df[df.iloc[:, 0].notna() & df.iloc[:, 3].notna()]
    if valid_data.empty:
        return None

    row = valid_data.iloc[-1]
    date_text = normalize_date(str(row.iloc[0]))

    try:
        weight_text = f"{float(str(row.iloc[3])):.1f}"
    except (TypeError, ValueError):
        return None

    upper = cell_at(row, 1)
    lower = cell_at(row, 2)
    blood_pressure = f"{upper}/{lower}" if upper != "-" and lower != "-" else "-"

    metrics = {
        "fat": cell_at(row, 5),
        "subq": cell_at(row, 7),
        "muscle": cell_at(row, 9),
        "visceral": cell_at(row, 11),
        "bmr": cell_at(row, 13),
        "age": cell_at(row, 15),
        "bmi": cell_at(row, 17),
        "bp": blood_pressure,
    }
    return date_text, weight_text, metrics


def build_timeline_entry(
    last_date: str,
    last_weight: str,
    metrics: Dict[str, str],
    existing_content: str,
) -> str:
    """新しい日次エントリ本文を作成します。"""
    new_entry = [format_header(last_date, last_weight), ""]
    new_entry.append("| 指標 | 値 | 指標 | 値 |")
    new_entry.append("| :--- | :--- | :--- | :--- |")
    new_entry.append(
        f"| 体脂肪 | {with_percent(metrics['fat'])} | 皮下脂肪 | {with_percent(metrics['subq'])} |"
    )
    new_entry.append(
        f"| 骨格筋 | {with_percent(metrics['muscle'])} | 内臓脂肪 | {metrics['visceral']} |"
    )
    new_entry.append(f"| 代謝 | {metrics['bmr']} | 体内年齢 | {metrics['age']} |")
    new_entry.append(f"| BMI | {metrics['bmi']} | 血圧 | {metrics['bp']} |")
    new_entry.append("")

    temp_record = WeightRecord(last_date, float(last_weight))
    existing_records = parse_existing_records(existing_content)
    all_records = [temp_record] + existing_records
    new_entry.append(generate_advice(all_records))
    new_entry.append("")
    new_entry.append("---")
    return "\n".join(new_entry)


def update_mermaid_chart(content: str, date_str: str, weight_val: str) -> str:
    """Mermaidチャートの x-axis / line に当日データを追記します。"""
    x_axis_match = re.search(r"x-axis \[(.*?)\]", content)
    if not x_axis_match:
        return content

    current_dates = x_axis_match.group(1)
    if date_str in current_dates:
        return content

    content = content.replace(
        f"x-axis [{current_dates}]",
        f"x-axis [{current_dates}, {date_str}]",
    )

    line_match = re.search(r"line \[(.*?)\]", content)
    if not line_match:
        return content

    current_vals = line_match.group(1)
    return content.replace(
        f"line [{current_vals}]",
        f"line [{current_vals}, {weight_val}]",
    )


def update_summary_section(content: str, records: List[WeightRecord]) -> str:
    """ファイル冒頭の「今日の振り返り」セクションを更新します。"""
    if not records:
        return content

    latest = records[0]
    previous = records[1] if len(records) > 1 else latest
    diff = latest.weight - previous.weight
    week_avg = statistics.mean([r.weight for r in records[:7]])

    content = re.sub(
        r"## 🧘‍♂️ 今日の振り返り \(\d+/\d+\)",
        f"## 🧘‍♂️ 今日の振り返り ({latest.date})",
        content,
    )

    diff_str = f"{diff:+.1f}kg" if diff else "±0.0kg"
    trend_emoji = "✨" if diff < 0 else "⚠️" if diff > 0 else "安定"
    summary_line = (
        f"> **最新体重**: {latest.weight}kg｜**前回比**: {diff_str} "
        f"{trend_emoji}｜**週間平均**: {week_avg:.1f}kg"
    )

    return re.sub(r"> \*\*最新体重\*\*: .*?\n", summary_line + "\n", content)


def insert_new_entry(content: str, entry: str) -> str:
    """タイムラインセクションに新規エントリを挿入します。"""
    if TIMELINE_MARKER in content:
        logger.info("タイムラインに新しいエントリを挿入しました。")
        return content.replace(TIMELINE_MARKER, f"{TIMELINE_MARKER}\n\n{entry}\n")
    logger.warning("タイムライン見出しが見つからないため末尾に追記します。")
    return f"{content.rstrip()}\n\n{entry}\n"


def main() -> int:
    logger.info("体重データ同期＆アドバイス生成を開始")

    df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
    if df is None:
        return 1

    latest = extract_latest_measurement(df)
    if latest is None:
        logger.error("有効なデータが見つかりませんでした。")
        return 1
    last_date, last_weight, metrics = latest

    content = utils.FileIO.read_text(TARGET_MD)
    if content is None:
        return 1

    if entry_exists(content, last_date):
        logger.info("既に記録済みです: %s", last_date)
    else:
        entry = build_timeline_entry(last_date, last_weight, metrics, content)
        content = insert_new_entry(content, entry)
        updated_records = parse_existing_records(content)
        content = update_summary_section(content, updated_records)

    content = update_mermaid_chart(content, last_date, last_weight)

    if utils.FileIO.write_text(TARGET_MD, content):
        logger.info("Markdownの更新が完了しました。")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
