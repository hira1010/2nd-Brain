#!/usr/bin/env python3
"""
資産データ同期スクリプト (Refactored Version)

Googleスプレッドシートから配当金・資産データを取得し、
Markdownファイルを自動更新します。
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from io import StringIO
import logging

try:
    import pandas as pd
    import requests
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません。")
    print("以下のコマンドを実行してください: pip install pandas requests")
    exit(1)

# === 設定 (Constants) ===
SHEET_ID = "1lnN_z84DLknNWbQX0YWzHiyn5Ea_Hue9TbxQeHSe3HA"
GID = "709056658"
# パスを共通管理可能に (将来的に manga_config へ移管も検討)
MD_FILE_PATH = r"c:\Users\hirak\Desktop\2nd-Brain\07_株\配当金・資産推移.md"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

# スプレッドシート内のデータ位置（ゼロベースインデックス）
YEAR_2026_COLUMN = 10  # K列
MONTH_START_ROW = 2    # 1月は3行目
TOTAL_ROW = 14         # 合計行
GROWTH_RATE_ROW = 15   # 伸び率行
ASSET_ROW = 16         # 資産行

# ログの設定
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("sync_assets")

def fetch_csv_data() -> pd.DataFrame:
    """
    スプレッドシートからCSVデータを取得し、DataFrameとして返す。
    """
    logger.info(f"データ取得中: {CSV_URL}")
    try:
        response = requests.get(CSV_URL, timeout=10)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), header=None)
    except requests.RequestException as e:
        logger.error(f"スプレッドシートの取得に失敗しました: {e}")
        raise

def format_value(value: Any) -> str:
    """
    数値を文字列に整形（0やNaNは'-'に変換）。
    """
    if pd.isna(value) or value == 0:
        return "-"
    # 小数点以下を削除
    return str(int(float(value))) if isinstance(value, (int, float)) else str(value)

def format_percentage(value: Any) -> str:
    """
    パーセンテージ値を整形。
    """
    if pd.isna(value):
        return "-"
    val_str = str(value).replace("%", "").strip()
    try:
        return f"{int(float(val_str))}%"
    except (ValueError, TypeError):
        return str(value)

def format_asset(value: Any) -> str:
    """
    資産値を整形（そのまま返す、または特定のフォーマットがあれば適用）。
    """
    if pd.isna(value):
        return "-"
    return str(value)

def extract_2026_data(df: pd.DataFrame) -> Dict[str, str]:
    """
    スプレッドシートから2026年のデータを抽出して整形。
    """
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
    summary_map = {
        "合計": (TOTAL_ROW, format_value),
        "伸び率": (GROWTH_RATE_ROW, format_percentage),
        "資産": (ASSET_ROW, format_asset)
    }
    
    for key, (row, func) in summary_map.items():
        try:
            val = df.iloc[row, YEAR_2026_COLUMN]
            data[key] = func(val)
        except IndexError:
            logger.warning(f"{key} のデータ抽出に失敗しました（範囲外）")
            data[key] = "-"
    
    return data

def update_month_row(line: str, value: str) -> str:
    """
    月別行の2026年カラムを更新。
    """
    parts = line.split('|')
    if len(parts) >= 12:
        # 値がある場合は太字、ない場合は通常
        formatted = f" **{value}** " if value != "-" else f" {value} "
        parts[11] = formatted
        return '|'.join(parts)
    return line

def update_summary_row(line: str, value: str, bold: bool = True) -> str:
    """
    サマリー行（合計・資産など）の2026年カラムを更新。
    """
    parts = line.split('|')
    if len(parts) >= 12:
        formatted = f" **{value}** " if bold else f" {value} "
        parts[11] = formatted
        return '|'.join(parts)
    return line

def update_markdown_table(content: str, data: Dict[str, str]) -> str:
    """
    Markdown内のテーブルを更新。
    """
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
    """
    メイン同期処理。
    """
    logger.info(f"資産データ同期を開始 (ターゲット: {MD_FILE_PATH})")
    
    try:
        # 1. データ取得
        df = fetch_csv_data()
        
        # 2. データ抽出
        data = extract_2026_data(df)
        logger.info(f"抽出完了 - 資産: {data.get('資産', '-')}, 伸び率: {data.get('伸び率', '-')}")
        
        # 3. Markdown更新
        with open(MD_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = update_markdown_table(content, data)
        
        with open(MD_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        logger.info("✓ 資産データの同期が完了しました。")
        return True
        
    except Exception as e:
        logger.error(f"同期中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = sync()
    sys.exit(0 if success else 1)
