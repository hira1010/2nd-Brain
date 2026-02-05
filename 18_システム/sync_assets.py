#!/usr/bin/env python3
"""
資産データ同期スクリプト

Googleスプレッドシートから配当金・資産データを取得し、
Markdownファイルを自動更新します。
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
from io import StringIO

try:
    import pandas as pd
    import requests
except ImportError:
    print("エラー: 必要なライブラリがインストールされていません。")
    print("以下のコマンドを実行してください: pip install pandas requests")
    exit(1)

# === 設定 ===
SHEET_ID = "1lnN_z84DLknNWbQX0YWzHiyn5Ea_Hue9TbxQeHSe3HA"
GID = "709056658"
MD_FILE_PATH = r"c:\Users\hirak\Desktop\2nd-Brain\07_株\配当金・資産推移.md"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

# スプレッドシート内のデータ位置（ゼロベースインデックス）
YEAR_2026_COLUMN = 10  # K列
MONTH_START_ROW = 2    # 1月は3行目
TOTAL_ROW = 14         # 合計行
GROWTH_RATE_ROW = 15   # 伸び率行
ASSET_ROW = 16         # 資産行


def fetch_csv_data() -> pd.DataFrame:
    """スプレッドシートからCSVデータを取得"""
    print(f"データ取得中: {CSV_URL}")
    response = requests.get(CSV_URL, timeout=10)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text), header=None)


def extract_2026_data(df: pd.DataFrame) -> Dict[str, str]:
    """2026年のデータを抽出して整形"""
    data = {}
    
    # 月別データ
    for i in range(12):
        month_name = f"{i+1}月"
        value = df.iloc[MONTH_START_ROW + i, YEAR_2026_COLUMN]
        data[month_name] = format_value(value)
    
    # 合計・伸び率・資産
    data["合計"] = format_value(df.iloc[TOTAL_ROW, YEAR_2026_COLUMN])
    data["伸び率"] = format_percentage(df.iloc[GROWTH_RATE_ROW, YEAR_2026_COLUMN])
    data["資産"] = format_asset(df.iloc[ASSET_ROW, YEAR_2026_COLUMN])
    
    return data


def format_value(value) -> str:
    """数値を文字列に整形（0やNaNは'-'に変換）"""
    if pd.isna(value) or value == 0:
        return "-"
    # 小数点以下を削除
    return str(int(float(value))) if isinstance(value, (int, float)) else str(value)


def format_percentage(value) -> str:
    """パーセンテージ値を整形"""
    if pd.isna(value):
        return "-"
    # "8%"形式で返す
    val_str = str(value).replace("%", "").strip()
    try:
        return f"{int(float(val_str))}%"
    except:
        return str(value)


def format_asset(value) -> str:
    """資産値を整形（"2200万"形式）"""
    if pd.isna(value):
        return "-"
    return str(value)


def update_markdown_table(content: str, data: Dict[str, str]) -> str:
    """Markdownテーブルを更新（フォーマットも修正）"""
    lines = content.splitlines()
    updated_lines = []
    
    for line in lines:
        # 月別行の更新
        month_match = re.match(r'^\| (\d{1,2})月 \|', line)
        if month_match:
            month_name = f"{month_match.group(1)}月"
            if month_name in data:
                line = update_month_row(line, data[month_name])
        
        # 合計・伸び率・資産行の更新
        elif "| **合計**" in line:
            line = update_summary_row(line, data["合計"], bold=True)
        elif "| 📈 **伸率**" in line and "合計" not in line:  # 最初の伸び率行（配当）
            line = update_summary_row(line, data["伸び率"], bold=False)
        elif "| 🏦 **資産**" in line:
            line = update_summary_row(line, data["資産"], bold=True)
        
        updated_lines.append(line)
    
    return "\n".join(updated_lines)


def update_month_row(line: str, value: str) -> str:
    """月別行の2026年カラムを更新"""
    parts = line.split('|')
    if len(parts) >= 12:
        # 値がある場合は太字、ない場合は通常
        formatted = f" **{value}** " if value != "-" else f" {value} "
        parts[11] = formatted
        return '|'.join(parts)
    return line


def update_summary_row(line: str, value: str, bold: bool = True) -> str:
    """合計・資産などのサマリー行を更新"""
    parts = line.split('|')
    if len(parts) >= 12:
        formatted = f" **{value}** " if bold else f" {value} "
        parts[11] = formatted
        return '|'.join(parts)
    return line


def sync() -> bool:
    """メイン同期処理"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 資産データ同期を開始...")
    
    try:
        # 1. データ取得
        df = fetch_csv_data()
        print(f"✓ データ取得完了（{len(df)}行）")
        
        # 2. 2026年データ抽出
        data = extract_2026_data(df)
        print(f"✓ 2026年データ抽出完了")
        print(f"  - 2月配当: {data['2月']}")
        print(f"  - 合計: {data['合計']}")
        
        # 3. Markdownファイル読み込み
        with open(MD_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ Markdownファイル読み込み完了")
        
        # 4. テーブル更新
        updated_content = update_markdown_table(content, data)
        
        # 5. 保存
        with open(MD_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✓ ファイル保存完了: {MD_FILE_PATH}")
        
        print("同期が正常に完了しました！")
        return True
        
    except requests.RequestException as e:
        print(f"✗ エラー: スプレッドシートへの接続に失敗しました")
        print(f"  詳細: {e}")
        return False
    except Exception as e:
        print(f"✗ エラー: 予期しない問題が発生しました")
        print(f"  詳細: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = sync()
    exit(0 if success else 1)
