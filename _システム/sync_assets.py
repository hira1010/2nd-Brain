#!/usr/bin/env python3
"""
資産データ同期スクリプト。
Googleスプレッドシートの2026年列を読み取り、Markdownテーブルを更新します。
"""

import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd

import os

# プロジェクトルートをパスに追加
_ROOT = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_ROOT) not in sys.path:
    sys.path.insert(0, os.path.dirname(_ROOT))

from lib import config, sheets, utils

SHEET_ID = config.ASSETS_SHEET_ID
GID = "709056658"
MD_FILE_PATH = config.STOCKS_DIR / "配当金・資産推移.md"

YEAR_2026_COLUMN = 10  # Spreadsheet column K
TARGET_TABLE_COLUMN = 11  # Markdown table "26" column

logger = utils.initialize_script("sync_assets")

@dataclass(frozen=True)
class AssetSnapshot:
    months: Dict[int, str]
    total: str
    growth_rate: str
    asset: str

def format_val(val: object, is_percent: bool = False) -> str:
    if pd.isna(val) or str(val).strip() in ("0", "0%"): return "-"
    s = str(val).strip().replace("%", "")
    try:
        return f"{int(float(s))}%" if is_percent else str(int(float(s)))
    except ValueError:
        return s

def update_table_cell(line: str, value: str, bold: bool = True) -> str:
    parts = line.split("|")
    if len(parts) <= TARGET_TABLE_COLUMN: return line
    parts[TARGET_TABLE_COLUMN] = f" **{value}** " if bold else f" {value} "
    return "|".join(parts)

def main() -> int:
    logger.info("資産データ同期開始")
    df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
    content = utils.FileIO.read_text(MD_FILE_PATH)
    if df is None or content is None: return 1

    # データ抽出
    months = {m: format_val(df.iloc[m + 1, YEAR_2026_COLUMN]) for m in range(1, 13)}
    total = format_val(df.iloc[14, YEAR_2026_COLUMN])
    growth = format_val(df.iloc[15, YEAR_2026_COLUMN], is_percent=True)
    asset = str(df.iloc[16, YEAR_2026_COLUMN]).strip()

    # Markdown更新 (ステートマシンを廃止し、より直感的に)
    lines = content.splitlines()
    in_target_table = False
    month_count = 0

    for i, line in enumerate(lines):
        if "17" in line and "26" in line:
            in_target_table = True; month_count = 0; continue
        if not in_target_table or not line.strip().startswith("|"):
            if month_count >= 15: in_target_table = False # 合計/増加率/資産の3行後
            continue
        
        # 月別行の判定 (先頭セルが数字)
        first_cell = line.split("|")[1].strip().replace("*", "")
        m = re.match(r"^(\d{1,2})", first_cell)
        if m:
            ml_idx = int(m.group(1))
            lines[i] = update_table_cell(line, months[ml_idx])
            month_count += 1
        elif month_count == 12: # 合計行
            lines[i] = update_table_cell(line, total)
            month_count += 1
        elif month_count == 13: # 増加率
            lines[i] = update_table_cell(line, growth, bold=False)
            month_count += 1
        elif month_count == 14: # 資産
            lines[i] = update_table_cell(line, asset)
            month_count += 1

    if utils.FileIO.write_text(MD_FILE_PATH, "\n".join(lines)):
        logger.info("同期完了")
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
