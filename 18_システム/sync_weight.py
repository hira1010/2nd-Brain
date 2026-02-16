#!/usr/bin/env python3
"""
体重データ同期＆振り返り統合スクリプト
Googleスプレッドシートから最新の体重を取得し、Markdownを更新するとともに、
過去の傾向からアドバイスを生成して追記します。
"""

import os
import sys
import re
import statistics
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# プロジェクトルートをパスに追加（libのインポート用）
lib_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if lib_parent not in sys.path:
    sys.path.append(lib_parent)

from lib import config, utils, sheets

# === 設定 ===
SHEET_ID = config.DIET_SHEET_ID
GID = "0"
TARGET_MD = config.DIET_DIR / "記録.md"
WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]

# ログ設定
logger = utils.setup_logger("sync_weight")

class WeightRecord:
    """体重記録データクラス"""
    def __init__(self, date: str, weight: float, waist: Optional[float] = None,
                 body_fat: Optional[float] = None, visceral_fat: Optional[float] = None):
        self.date = date
        self.weight = weight
        self.waist = waist
        self.body_fat = body_fat
        self.visceral_fat = visceral_fat
    
    def __repr__(self):
        return f"WeightRecord({self.date}, {self.weight}kg)"

def normalize_date(date_text: str) -> str:
    """日付テキストの '01/01' 形式を '1/1' に正規化します。"""
    return re.sub(r"/0", "/", str(date_text).strip())

def format_header(date_text: str, weight: str) -> str:
    """タイムライン用のヘッダーを作成します。"""
    normalized = normalize_date(date_text)
    try:
        # 年は2026固定（システムの仕様）
        dt = datetime.strptime(f"2026/{normalized}", "%Y/%m/%d")
        return f"### {dt.month}/{dt.day} ({WEEKDAYS[dt.weekday()]}) ── **{weight}**kg"
    except ValueError:
        return f"### {normalized} ── **{weight}**kg"

def parse_existing_records(content: str) -> List[WeightRecord]:
    """Markdownから既存の記録を抽出します。"""
    records = []
    # 日次記録のパターン
    pattern = r'###\s+(\d+)/(\d+)\s+\([^)]+\)\s+──\s+\*\*([0-9.]+)\*\*kg(?:\s+/\s+\*\*([0-9.]+)\*\*cm)?'
    
    matches = re.finditer(pattern, content)
    for match in matches:
        month = int(match.group(1))
        day = int(match.group(2))
        weight = float(match.group(3))
        waist = float(match.group(4)) if match.group(4) else None
        date_str = f"{month}/{day}"
        
        # 詳細（体脂肪など）をその後のセクションから取得
        section_start = match.end()
        next_match = re.search(r'###\s+\d+/\d+', content[section_start:])
        section_end = section_start + next_match.start() if next_match else len(content)
        section = content[section_start:section_end]
        
        body_fat = None
        visceral_fat = None
        bf_match = re.search(r'体脂肪:\s*([0-9.]+)%', section)
        if bf_match: body_fat = float(bf_match.group(1))
        vf_match = re.search(r'内臓脂肪:\s*([0-9.]+)', section)
        if vf_match: visceral_fat = float(vf_match.group(1))
        
        records.append(WeightRecord(date_str, weight, waist, body_fat, visceral_fat))
    
    # 日付順（新しい順）にソート
    return sorted(records, key=lambda r: tuple(map(int, r.date.split('/'))), reverse=True)

def generate_advice(records: List[WeightRecord]) -> str:
    """最新データに基づいたアドバイスを生成します。"""
    if len(records) < 2:
        return "データが不足しています。継続して記録しましょう。"
    
    latest = records[0]
    previous = records[1]
    diff = latest.weight - previous.weight
    
    recent_weights = [r.weight for r in records[:7]]
    week_avg = statistics.mean(recent_weights)
    
    advice_lines = [
        "## 🎯 今日の振り返りとアドバイス\n",
        f"**日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n",
        "### 📊 体重推移の分析\n",
        f"- **最新体重**: {latest.weight}kg"
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

def update_mermaid_chart(content: str, date_str: str, weight_val: str) -> str:
    """Mermaidチャートのデータを更新します。"""
    x_axis_match = re.search(r"x-axis \[(.*?)\]", content)
    date_added = False
    if x_axis_match:
        current_dates = x_axis_match.group(1)
        if date_str not in current_dates:
            new_dates = f"{current_dates}, {date_str}"
            content = content.replace(f"x-axis [{current_dates}]", f"x-axis [{new_dates}]")
            date_added = True

    line_match = re.search(r"line \[(.*?)\]", content)
    if line_match and date_added:
        current_vals = line_match.group(1)
        new_vals = f"{current_vals}, {weight_val}"
        content = content.replace(f"line [{current_vals}]", f"line [{new_vals}]")

    return content

def update_summary_section(content: str, records: List[WeightRecord]) -> str:
    """ファイル冒頭の「今日の振り返り」セクションを更新します。"""
    if not records: return content
    
    latest = records[0]
    previous = records[1] if len(records) > 1 else latest
    diff = latest.weight - previous.weight
    recent_weights = [r.weight for r in records[:7]]
    week_avg = statistics.mean(recent_weights)
    
    # 日付ヘッダーの更新
    content = re.sub(r'## 🧘‍♂️ 今日の振り返り \(\d+/\d+\)', f'## 🧘‍♂️ 今日の振り返り ({latest.date})', content)
    
    # 数値ラインの更新
    diff_str = f"{diff:+.1f}kg" if diff != 0 else "±0.0kg"
    trend_emoji = "✨" if diff < 0 else "⚠️" if diff > 0 else "安定"
    new_summary_line = f"> **最新体重**: {latest.weight}kg｜**前回比**: {diff_str} {trend_emoji}｜**週間平均**: {week_avg:.1f}kg"
    
    content = re.sub(r'> \*\*最新体重\*\*: .*?\n', new_summary_line + "\n", content)
    
    return content

def main():
    logger.info("体重データ同期＆アドバイス生成を開始")
    
    # 1. スプレッドシートから最新データを取得
    df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
    if df is None:
        return 1
    
    # 最新の（最後の）有効行を取得
    # スプレッドシートの構造: 0:日付, 1:血圧上, 2:血圧下, 3:体重 ...
    valid_data = df[df.iloc[:, 0].notna() & df.iloc[:, 3].notna()]
    if valid_data.empty:
        logger.error("有効なデータが見つかりませんでした。")
        return 1
    
    last_row = valid_data.iloc[-1]
    last_date = str(last_row[0])
    last_weight = str(last_row[3])
    
    # 指標の抽出
    def get_val(idx):
        try:
            v = last_row[idx]
            import pandas as pd
            return str(v) if pd.notna(v) else "-"
        except: return "-"

    metrics = {
        "fat": get_val(5),
        "subq": get_val(7),
        "muscle": get_val(9),
        "visceral": get_val(11),
        "bmr": get_val(13),
        "age": get_val(15),
        "bmi": get_val(17),
        "bp": f"{get_val(1)}/{get_val(2)}" if get_val(1) != "-" else "-"
    }
    
    # 2. Markdownファイルの読み込み
    content = utils.FileIO.read_text(TARGET_MD)
    if content is None:
        return 1
    
    header_str = f"### {last_date} ({WEEKDAYS[datetime.strptime('2026/'+last_date, '%Y/%m/%d').weekday()]}) — {last_weight}kg"
    
    # 重複チェック
    if header_str in content:
        logger.info(f"既に記録済みです: {last_date}")
    else:
        # 新規エントリの作成
        insert_marker = "## 🗓️ タイムライン"
        new_entry = f"\n\n{header_str}\n\n"
        new_entry += "| 指標 | 値 | 指標 | 値 |\n"
        new_entry += "| :--- | :--- | :--- | :--- |\n"
        new_entry += f"| 体脂肪 | {metrics['fat']}% | 皮下脂肪 | {metrics['subq']}% |\n"
        new_entry += f"| 骨格筋 | {metrics['muscle']}% | 内臓脂肪 | {metrics['visceral']} |\n"
        new_entry += f"| 代謝 | {metrics['bmr']} | 体内年齢 | {metrics['age']} |\n"
        new_entry += f"| BMI | {metrics['bmi']} | 血圧 | {metrics['bp']} |\n\n"
        
        # アドバイスの生成
        temp_record = WeightRecord(normalize_date(last_date), float(last_weight))
        existing_records = parse_existing_records(content)
        all_records = [temp_record] + existing_records
        advice = generate_advice(all_records)
        
        new_entry += advice + "\n\n---\n"
        
        if insert_marker in content:
            content = content.replace(insert_marker, f"{insert_marker}\n{new_entry}")
            logger.info("タイムラインに新しいエントリを挿入しました。")
            
            # トップのサマリーセクションも更新
            content = update_summary_section(content, all_records)

    # 3. Mermaidチャートの更新
    content = update_mermaid_chart(content, normalize_date(last_date), last_weight)
    
    # 4. 保存
    success = utils.FileIO.write_text(TARGET_MD, content)
    if success:
        logger.info("Markdownの更新が完了しました。")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
