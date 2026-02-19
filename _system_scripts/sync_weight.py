#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 体重データ同期＆振り返りスクリプト (Integrated with Sheets)

Googleスプレッドシートから最新の計測データを取得し、「記録.md」を更新します。
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
from datetime import datetime
from typing import List, Dict, Optional
import statistics
import pandas as pd

from lib import config, utils, sheets

# 初期化 (UTF-8, Logger)
logger = utils.initialize_script("sync_weight")


class WeightRecord:
    """体重記録データクラス"""
    def __init__(self, date: str, weight: float, body_fat: Optional[float] = None,
                 muscle: Optional[float] = None, metabolism: Optional[float] = None,
                 systolic: Optional[int] = None, diastolic: Optional[int] = None,
                 waist: Optional[float] = None):
        self.date = date
        self.weight = weight
        self.body_fat = body_fat
        self.muscle = muscle
        self.metabolism = metabolism
        self.systolic = systolic
        self.diastolic = diastolic
        self.waist = waist
    
    def __repr__(self):
        return f"WeightRecord({self.date}, {self.weight}kg)"


class DietAnalyzer:
    """ダイエットデータ分析・同期クラス"""
    
    def __init__(self, record_file: Path):
        self.record_file = record_file
        self.records: List[WeightRecord] = []
        self.start_weight = 94.0
        self.target_weight = 76.0
        
    def fetch_records_from_sheets(self) -> List[WeightRecord]:
        """スプレッドシートからデータを取得"""
        logger.info("🌐 スプレッドシートから最新データを取得しています...")
        df = sheets.fetch_csv_from_google_sheets(config.DIET_SHEET_ID, "0")
        if df is None:
            logger.error("❌ スプレッドシートの取得に失敗しました。")
            return []

        new_records = []
        # 列のインデックスはシートの構造に依存 (例: 0=日付, 3=体重CT, 5=体脂肪, 6=骨格筋, 7=代謝, 8=血圧上, 9=血圧下)
        # 取得したCSVのサンプルに基づいてパース (ヘッダーを考慮)
        for _, row in df.iterrows():
            date_val = str(row[0]).replace("-", "/")
            if not re.match(r'^\d{1,2}/\d{1,2}$', date_val):
                continue
            
            try:
                weight = float(str(row[3]).replace(",", ""))
                body_fat = float(str(row[5]).replace(",", "")) if pd.notna(row[5]) and str(row[5]) != "-" else None
                muscle = float(str(row[6]).replace(",", "")) if pd.notna(row[6]) and str(row[6]) != "-" else None
                metabolism = int(float(str(row[7]).replace(",", ""))) if pd.notna(row[7]) and str(row[7]) != "-" else None
                systolic = int(float(str(row[8]).replace(",", ""))) if pd.notna(row[8]) and str(row[8]) != "-" else None
                diastolic = int(float(str(row[9]).replace(",", ""))) if pd.notna(row[9]) and str(row[9]) != "-" else None
                
                new_records.append(WeightRecord(
                    date=date_val, weight=weight, body_fat=body_fat,
                    muscle=muscle, metabolism=metabolism,
                    systolic=systolic, diastolic=diastolic
                ))
            except (ValueError, TypeError):
                continue

        # 日付順（降順）にソート
        self.records = sorted(new_records, key=lambda r: tuple(map(int, r.date.split('/'))), reverse=True)
        return self.records

    def update_record_md(self):
        """記録.mdのテーブルとタイムラインを更新"""
        content = utils.FileIO.read_text(self.record_file)
        if not content or not self.records:
            return

        latest = self.records[0]
        
        # 1. タイムラインセクションの更新（その日のセクションがなければ追加）
        date_header = f"### {latest.date}"
        if date_header not in content:
            logger.info("📝 新しい日付セクションを追加します: %s", latest.date)
            new_section = self._format_timeline_section(latest)
            # ## 🗓️ タイムライン の直後に挿入
            content = content.replace("## 🗓️ タイムライン\n", f"## 🗓️ タイムライン\n\n{new_section}\n")

        # 2. テーブルの更新
        content = self._update_table(content)

        # 3. グラフ(Mermaid)の更新
        content = self._update_mermaid_graph(content)

        utils.FileIO.write_text(self.record_file, content, make_backup=True)

    def _format_timeline_section(self, record: WeightRecord) -> str:
        bp_str = f"{record.systolic}/{record.diastolic}" if record.systolic else "-"
        return f"""{record.date} ({datetime.now().strftime('%a')}) — {record.weight}kg

| 指標 | 値 | 指標 | 値 |
| :--- | :--- | :--- | :--- |
| 体脂肪 | {record.body_fat}% | 血圧 | {bp_str} |
| 骨格筋 | {record.muscle}% | 代謝 | {record.metabolism} |
| BMI | {(record.weight / (1.79**2)):.1f} | - | - |

> **メモ**: (自動同期)"""

    def _update_table(self, content: str) -> str:
        # テーブル部分を抽出
        table_pattern = r'(\| 日付 \| 体重 \| 前日比 \| 血圧 \(上/下\) \|\n\| :--- \| :--- \| :--- \| :--- \|\n)([\s\S]*?)\n\n'
        match = re.search(table_pattern, content)
        if not match:
            return content
        
        header_and_align = match.group(1)
        # 既存のテーブル行から最新数件を取得
        rows = []
        for r in self.records[:10]:
            prev_weight = next((rec.weight for rec in self.records if self.records.index(rec) == self.records.index(r) + 1), None)
            diff_str = "-"
            if prev_weight:
                diff = r.weight - prev_weight
                diff_str = f"{'+' if diff > 0 else '−'}{abs(diff):.1f}"
            
            bp_str = f"{r.systolic}/{r.diastolic}" if r.systolic else "-"
            rows.append(f"| {r.date} | {r.weight}kg | {diff_str} | {bp_str} |")
        
        new_table = header_and_align + "\n".join(rows) + "\n\n"
        return content.replace(match.group(0), new_table)

    def _update_mermaid_graph(self, content: str) -> str:
        # グラフ用のデータを直近20件から作成
        subset = self.records[:20][::-1] # 昇順
        dates = [r.date for r in subset]
        weights = [str(r.weight) for r in subset]
        
        x_axis = f"    x-axis [{', '.join(dates)}]"
        line_data = f"    line [{', '.join(weights)}]"
        
        content = re.sub(r'x-axis \[.*?\]', x_axis, content)
        content = re.sub(r'line \[.*?\]', line_data, content)
        return content

    def analyze_trend(self) -> Dict:
        if len(self.records) < 2:
            return {"status": "データ不足"}
        
        latest = self.records[0]
        previous = self.records[1]
        diff = latest.weight - previous.weight
        week_avg = statistics.mean([r.weight for r in self.records[:7]])
        remaining = latest.weight - self.target_weight
        progress = ((self.start_weight - latest.weight) / (self.start_weight - self.target_weight)) * 100
        
        return {
            "latest": latest, "diff": diff, "week_avg": week_avg,
            "remaining": remaining, "progress": progress
        }

    def generate_advice(self, analysis: Dict) -> str:
        advice = f"""## 🧘‍♂️ 今日の振り返り ({analysis['latest'].date})

> **最新体重**: {analysis['latest'].weight}kg｜**前回比**: {analysis['diff']:+.1f}kg｜**週間平均**: {analysis['week_avg']:.1f}kg

### アクションプラン

> 「失われた身体機能を呼び戻す」 — Ninniki-nene Style

- ✅ 現在のリズムをキープ！
- ✅ 水分補給を適切に
- ✅ 1時間に1回、姿勢リセット

> [!TIP]
> "測る行為そのものが健康への第一歩。今日も、本来の自分を取り戻しましょう！" """
        return advice

    def inject_advice(self, advice: str):
        content = utils.FileIO.read_text(self.record_file)
        if not content: return
        
        # 既存の「今日の振り返り」セクションを置換
        pattern = r'## 🧘‍♂️ 今日の振り返り \(\d+/\d+\)[\s\S]*?(?=\n---)'
        content = re.sub(pattern, advice + "\n", content)
        utils.FileIO.write_text(self.record_file, content)


def main():
    logger.info("🏥 体重データ自動同期開始")
    analyzer = DietAnalyzer(config.DIET_RECORD_FILE)
    
    records = analyzer.fetch_records_from_sheets()
    if not records:
        return
    
    analyzer.update_record_md()
    analysis = analyzer.analyze_trend()
    if analysis.get("status") != "データ不足":
        advice = analyzer.generate_advice(analysis)
        analyzer.inject_advice(advice)
        logger.info("✅ 同期と分析が完了しました。")
    
    logger.info("🎉 Done!")


if __name__ == "__main__":
    main()
