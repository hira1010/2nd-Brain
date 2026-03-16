#!/usr/bin/env python3
"""
体重データ同期＆振り返り統合スクリプト。
Googleスプレッドシートから最新の体重を取得し、Markdownを更新します。
"""

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

import os

# プロジェクトルートをパスに追加（libのインポート前に行う必要あり）
_ROOT = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_ROOT) not in sys.path:
    sys.path.insert(0, os.path.dirname(_ROOT))

from lib import config, sheets, utils
from lib.markdown import MarkdownEditor

SHEET_ID = config.DIET_SHEET_ID
TARGET_MD = config.DIET_DIR / "記録.md"
TARGET_YEAR = 2026
WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
TIMELINE_MARKER = "## 🗓️ タイムライン"

logger = utils.initialize_script("sync_weight")
MetricMap = Dict[str, str]

@dataclass(frozen=True)
class WeightRecord:
    date: str
    weight: float
    body_fat: Optional[float] = None
    visceral_fat: Optional[float] = None

    @property
    def sort_key(self) -> Tuple[int, int]:
        month, day = self.date.split("/")
        return int(month), int(day)

# --- ユーティリティ ---

def normalize_date(date_text: str) -> str:
    raw = str(date_text).strip()
    return re.sub(r"/0", "/", raw) if "/" in raw else raw

def format_header(date_text: str, weight: float) -> str:
    norm = normalize_date(date_text)
    try:
        dt = datetime.strptime(f"{TARGET_YEAR}/{norm}", "%Y/%m/%d")
        return f"### {dt.month}/{dt.day} ({WEEKDAYS[dt.weekday()]}) ── {weight:.1f}kg"
    except ValueError:
        return f"### {norm} ── {weight:.1f}kg"

# --- データ抽出 ---

def extract_latest_measurement(df: pd.DataFrame) -> Optional[Tuple[str, float, MetricMap]]:
    valid = df[df.iloc[:, 0].notna() & df.iloc[:, 3].notna()]
    if valid.empty: return None
    row = valid.iloc[-1]
    try:
        date_text = normalize_date(str(row.iloc[0]))
        weight = float(str(row.iloc[4]))
        metrics = {name: str(row.iloc[idx]) if not pd.isna(row.iloc[idx]) else "-" 
                  for name, idx in {"fat":6, "subq":8, "muscle":10, "visceral":12, "bmr":14, "age":16, "bmi":18}.items()}
        # 血圧
        u, l = row.iloc[1], row.iloc[2]
        metrics["bp"] = f"{u}/{l}" if not (pd.isna(u) or pd.isna(l)) else "-"
        return date_text, weight, metrics
    except (ValueError, IndexError):
        return None

# --- メインロジック ---

def main() -> int:
    logger.info("体重データ同期開始")
    df = sheets.fetch_csv_from_google_sheets(SHEET_ID)
    content = utils.FileIO.read_text(TARGET_MD)
    if df is None or content is None: return 1

    latest = extract_latest_measurement(df)
    if not latest: return 1
    date_str, weight_val, metrics = latest

    editor = MarkdownEditor(content)
    
    # 重複チェック用正規表現
    if re.search(rf"^###\s+{re.escape(date_str)}\b", content, re.MULTILINE):
        logger.info("既に記録済み: %s", date_str)
    else:
        # エントリ構築
        entry = [format_header(date_str, weight_val), "", "| 指標 | 値 | 指標 | 値 |", "| :--- | :--- | :--- | :--- |"]
        entry.append(f"| 体脂肪 | {metrics['fat']}% | 皮下脂肪 | {metrics['subq']}% |")
        entry.append(f"| 骨格筋 | {metrics['muscle']}% | 内臓脂肪 | {metrics['visceral']} |")
        entry.append(f"| 代謝 | {metrics['bmr']} | 体内年齢 | {metrics['age']} |")
        entry.append(f"| BMI | {metrics['bmi']} | 血圧 | {metrics['bp']} |")
        entry.append("\n## 🎯 今日のアドバイス\n> 身体の本来の機能を取り戻しましょう！\n\n---")
        
        editor.insert_after_marker(TIMELINE_MARKER, "\n".join(entry))
        # サマリー更新 (簡易版)
        editor.content = re.sub(r"## 🧘‍♂️ 今日の振り返り \(.*?\)", f"## 🧘‍♂️ 今日の振り返り ({date_str})", editor.content)

    # チャート更新
    editor.update_mermaid_array("x-axis", date_str)
    editor.update_mermaid_array("line", str(weight_val))

    if utils.FileIO.write_text(TARGET_MD, editor.get_content()):
        logger.info("同期完了")
        return 0
    return 1

import re # normalize_date で使用
if __name__ == "__main__":
    raise SystemExit(main())
