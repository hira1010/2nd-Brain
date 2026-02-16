#!/usr/bin/env python3
"""
資産データ同期スクリプト
Googleスプレッドシートから配当金・資産データを取得し、Markdownファイルを自動更新します。
"""

import os
import sys
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# プロジェクトルートをパスに追加（libのインポート用）
lib_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if lib_parent not in sys.path:
    sys.path.append(lib_parent)

from lib import config, utils, sheets

# === 設定 ===
# lib/config から値を引き継ぎつつ、このスクリプト固有のGIDなどを定義
SHEET_ID = config.ASSETS_SHEET_ID
GID = "709056658"
# ターゲットとなるMarkdownファイルのパス
MD_FILE_PATH = config.STOCKS_DIR / "配当金・資産推移.md"

# スプレッドシート内のデータ位置（ゼロベースインデックス）
YEAR_2026_COLUMN = 10  # K列
MONTH_START_ROW = 2    # 1月は3行目
TOTAL_ROW = 14         # 合計行
GROWTH_RATE_ROW = 15   # 伸び率行
ASSET_ROW = 16         # 資産行

logger = utils.setup_logger("sync_assets")

def format_value(value: Any) -> str:
    """数値を文字列に整形（0やNaNは'-'に変換）。"""
    import pandas as pd
    if pd.isna(value) or value == 0:
        return "-"
    return str(int(float(value))) if isinstance(value, (int, float)) else str(value)

def format_percentage(value: Any) -> str:
    """パーセンテージ値を整形。"""
    import pandas as pd
    if pd.isna(value):
        return "-"
    val_str = str(value).replace("%", "").strip()
    try:
        return f"{int(float(val_str))}%"
    except (ValueError, TypeError):
        return str(value)

def format_asset(value: Any) -> str:
    """資産値を整形。"""
    import pandas as pd
    if pd.isna(value):
        return "-"
    return str(value)

def extract_2026_data(df) -> Dict[str, str]:
    """スプレッドシートから2026年のデータを抽出して整形。"""
    data = {}
    
    # 月別データ
    for i in range(12):
        month_key = f"{i+1}月"
        try:
            val = df.iloc[MONTH_START_ROW + i, YEAR_2026_COLUMN]
            data[month_key] = format_value(val)
        except IndexError:
            logger.warning(f"{month_key} のデータ抽出に失敗しました（範囲外）")
            data[month_key] = "-"
    
    # サマリーデータ
    summary_config = {
        "合計": (TOTAL_ROW, format_value),
        "伸び率": (GROWTH_RATE_ROW, format_percentage),
        "資産": (ASSET_ROW, format_asset)
    }
    
    for key, (row, func) in summary_config.items():
        try:
            val = df.iloc[row, YEAR_2026_COLUMN]
            data[key] = func(val)
        except IndexError:
            logger.warning(f"{key} のデータ抽出に失敗しました（範囲外）")
            data[key] = "-"
    
    return data

def update_month_row(line: str, value: str) -> str:
    """月別行の2026年カラムを更新。"""
    parts = line.split('|')
    if len(parts) >= 12:
        formatted = f" **{value}** " if value != "-" else f" {value} "
        parts[11] = formatted
        return '|'.join(parts)
    return line

def update_summary_row(line: str, value: str, bold: bool = True) -> str:
    """サマリー行（合計・資産など）の2026年カラムを更新。"""
    parts = line.split('|')
    if len(parts) >= 12:
        formatted = f" **{value}** " if bold else f" {value} "
        parts[11] = formatted
        return '|'.join(parts)
    return line

def update_markdown_table(content: str, data: Dict[str, str]) -> str:
    """Markdown内のテーブルを更新。"""
    lines = content.splitlines()
    updated_lines = []
    
    for line in lines:
        # 月別行の更新
        month_match = re.match(r'^\| (\d{1,2})月 \|', line)
        if month_match:
            month_name = f"{month_match.group(1)}月"
            if month_name in data:
                line = update_month_row(line, data[month_name])
        
        # サマリー行の更新
        elif "| **合計**" in line:
            line = update_summary_row(line, data["合計"], bold=True)
        elif "| 📈 **伸率**" in line and "合計" not in line:
            line = update_summary_row(line, data["伸び率"], bold=False)
        elif "| 🏦 **資産**" in line:
            line = update_summary_row(line, data["資産"], bold=True)
        
        updated_lines.append(line)
    
    return "\n".join(updated_lines)

def sync() -> bool:
    """メイン同期処理。"""
    logger.info(f"資産データ同期を開始 (ターゲット: {MD_FILE_PATH})")
    
    try:
        # 1. データ取得
        df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
        if df is None:
            return False
            
        # 2. データ抽出
        data = extract_2026_data(df)
        logger.info(f"抽出完了 - 資産: {data.get('資産', '-')}, 伸び率: {data.get('伸び率', '-')}")
        
        # 3. Markdown更新
        content = utils.FileIO.read_text(MD_FILE_PATH)
        if content is None:
            return False
        
        updated_content = update_markdown_table(content, data)
        success = utils.FileIO.write_text(MD_FILE_PATH, updated_content)
        
        if success:
            logger.info("✓ 資産データの同期が完了しました。")
        return success
        
    except Exception as e:
        logger.error(f"同期中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    success = sync()
    sys.exit(0 if success else 1)
