#!/usr/bin/env python3
"""
資産データ同期スクリプト。
Googleスプレッドシートの2026年列を読み取り、Markdownテーブルを更新します。
"""

import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd

LIB_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LIB_PARENT not in sys.path:
    sys.path.append(LIB_PARENT)

from lib import config, sheets, utils

SHEET_ID = config.ASSETS_SHEET_ID
GID = "709056658"
MD_FILE_PATH = config.STOCKS_DIR / "配当金・資産推移.md"

YEAR_2026_COLUMN = 10  # Spreadsheet column K
MONTH_START_ROW = 2
TOTAL_ROW = 14
GROWTH_RATE_ROW = 15
ASSET_ROW = 16
TARGET_TABLE_COLUMN = 11  # Markdown table "26" column

logger = utils.setup_logger("sync_assets")


@dataclass(frozen=True)
class AssetSnapshot:
    """同期対象の年次スナップショット。"""

    months: Dict[int, str]
    total: str
    growth_rate: str
    asset: str


def format_count(value: object) -> str:
    """配当金などの整数値を文字列化。0/欠損は '-'。"""
    if pd.isna(value):
        return "-"
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    if num == 0:
        return "-"
    return str(int(num))


def format_percentage(value: object) -> str:
    """増加率を '9%' 形式で返す。欠損は '-'。"""
    if pd.isna(value):
        return "-"
    text = str(value).replace("%", "").strip()
    try:
        return f"{int(float(text))}%"
    except (TypeError, ValueError):
        return str(value)


def format_asset(value: object) -> str:
    """資産の表示値を返す。欠損は '-'。"""
    if pd.isna(value):
        return "-"
    return str(value).strip()


def read_cell(df: pd.DataFrame, row: int, col: int) -> object:
    """範囲外アクセスを '-' にフォールバック。"""
    try:
        return df.iloc[row, col]
    except IndexError:
        return pd.NA


def extract_snapshot(df: pd.DataFrame) -> AssetSnapshot:
    """2026年列から月次/サマリー値を抽出。"""
    months: Dict[int, str] = {}
    for month in range(1, 13):
        row = MONTH_START_ROW + (month - 1)
        months[month] = format_count(read_cell(df, row, YEAR_2026_COLUMN))

    total = format_count(read_cell(df, TOTAL_ROW, YEAR_2026_COLUMN))
    growth_rate = format_percentage(read_cell(df, GROWTH_RATE_ROW, YEAR_2026_COLUMN))
    asset = format_asset(read_cell(df, ASSET_ROW, YEAR_2026_COLUMN))
    return AssetSnapshot(months=months, total=total, growth_rate=growth_rate, asset=asset)


def update_table_cell(line: str, value: str, bold: bool = True) -> str:
    """Markdown表の対象列を更新。"""
    parts = line.split("|")
    if len(parts) <= TARGET_TABLE_COLUMN:
        return line
    parts[TARGET_TABLE_COLUMN] = f" **{value}** " if bold else f" {value} "
    return "|".join(parts)


def is_month_row(first_cell: str) -> Optional[int]:
    """先頭セルから月番号を抽出。"""
    m = re.match(r"^\s*(\d{1,2})\D*$", first_cell.strip())
    if not m:
        return None
    month = int(m.group(1))
    if 1 <= month <= 12:
        return month
    return None


def update_markdown_table(content: str, snapshot: AssetSnapshot) -> str:
    """
    年次テーブルを更新。
    文字列見出しに依存せず、月行の直後3行を
    `total -> growth_rate -> asset` とみなして更新する。
    """
    lines = content.splitlines()
    in_table = False
    month_rows_seen = 0
    summary_phase = 0

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if not stripped.startswith("|"):
            in_table = False
            continue

        parts = line.split("|")
        if len(parts) <= TARGET_TABLE_COLUMN:
            continue

        first_cell = parts[1].strip().replace("*", "")

        if "17" in line and "26" in line:
            in_table = True
            month_rows_seen = 0
            summary_phase = 0
            continue

        if not in_table:
            continue

        month = is_month_row(first_cell)
        if month is not None:
            lines[idx] = update_table_cell(line, snapshot.months[month], bold=True)
            month_rows_seen += 1
            if month_rows_seen == 12:
                summary_phase = 1
            continue

        if summary_phase == 1:
            lines[idx] = update_table_cell(line, snapshot.total, bold=True)
            summary_phase = 2
            continue
        if summary_phase == 2:
            lines[idx] = update_table_cell(line, snapshot.growth_rate, bold=False)
            summary_phase = 3
            continue
        if summary_phase == 3:
            lines[idx] = update_table_cell(line, snapshot.asset, bold=True)
            in_table = False

    return "\n".join(lines)


def sync() -> bool:
    """資産データを同期してMarkdownへ反映。"""
    logger.info("資産データ同期開始: %s", MD_FILE_PATH)

    df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
    if df is None:
        return False

    snapshot = extract_snapshot(df)
    logger.info(
        "抽出値: 資産=%s, 増加率=%s, 合計=%s",
        snapshot.asset,
        snapshot.growth_rate,
        snapshot.total,
    )

    content = utils.FileIO.read_text(MD_FILE_PATH)
    if content is None:
        return False

    updated = update_markdown_table(content, snapshot)
    if not utils.FileIO.write_text(MD_FILE_PATH, updated):
        return False

    logger.info("資産データ同期が完了しました。")
    return True


def main() -> int:
    return 0 if sync() else 1


if __name__ == "__main__":
    raise SystemExit(main())
