#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 体重データ同期＆振り返りスクリプト

このスクリプトは「記録.md」から体重データを読み取り、
推移分析と今日のアドバイスを自動生成します。
"""

import os
import sys
import io

# Windows環境でのエンコーディング問題を回避
if sys.platform == 'win32':
    # 標準出力・標準エラー出力をUTF-8で再定義
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import statistics

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

class DietAnalyzer:
    """ダイエットデータ分析クラス"""
    
    def __init__(self, record_file: Path):
        self.record_file = record_file
        self.records: List[WeightRecord] = []
        self.start_weight = 94.0  # 初期値
        self.target_weight = 76.0  # 目標
        
    def parse_records(self) -> List[WeightRecord]:
        """記録.mdから体重データを抽出"""
        if not self.record_file.exists():
            print(f"⚠️ ファイルが見つかりません: {self.record_file}")
            return []
        
        content = self.record_file.read_text(encoding='utf-8')
        records = []
        
        # 日次記録のパターン: ### 2/5 (木) ── **94.3**kg
        pattern = r'###\s+(\d+)/(\d+)\s+\([^)]+\)\s+──\s+\*\*([0-9.]+)\*\*kg(?:\s+/\s+\*\*([0-9.]+)\*\*cm)?'
        
        matches = re.finditer(pattern, content)
        for match in matches:
            month = int(match.group(1))
            day = int(match.group(2))
            weight = float(match.group(3))
            waist = float(match.group(4)) if match.group(4) else None
            
            # 日付文字列を生成（現在の年を仮定）
            date_str = f"{month}/{day}"
            
            # その日の詳細データを探す
            # 次の日次記録までのセクションを取得
            section_start = match.end()
            next_match = re.search(r'###\s+\d+/\d+', content[section_start:])
            section_end = section_start + next_match.start() if next_match else len(content)
            section = content[section_start:section_end]
            
            # 体脂肪率などの詳細データを抽出
            body_fat = None
            visceral_fat = None
            details = re.search(r'体脂肪:\s*([0-9.]+)%', section)
            if details:
                body_fat = float(details.group(1))
            visceral = re.search(r'内臓脂肪:\s*([0-9.]+)', section)
            if visceral:
                visceral_fat = float(visceral.group(1))
            
            records.append(WeightRecord(date_str, weight, waist, body_fat, visceral_fat))
        
        # 日付順にソート（新しい順）
        self.records = sorted(records, key=lambda r: tuple(map(int, r.date.split('/'))), reverse=True)
        return self.records
    
    def analyze_trend(self) -> Dict[str, any]:
        """体重推移を分析"""
        if len(self.records) < 2:
            return {"status": "データ不足", "message": "比較するデータがありません"}
        
        latest = self.records[0]
        previous = self.records[1]
        
        # 前回比
        diff = latest.weight - previous.weight
        diff_percent = (diff / previous.weight) * 100
        
        # 週間平均（直近7件）
        recent_weights = [r.weight for r in self.records[:7]]
        week_avg = statistics.mean(recent_weights) if recent_weights else latest.weight
        
        # トレンド判定
        if len(self.records) >= 3:
            recent_3 = [r.weight for r in self.records[:3]]
            trend = "減少傾向" if recent_3[0] < recent_3[-1] else "横ばいor増加"
        else:
            trend = "評価中"
        
        # 目標までの距離
        remaining = latest.weight - self.target_weight
        progress = ((self.start_weight - latest.weight) / (self.start_weight - self.target_weight)) * 100
        
        return {
            "latest": latest,
            "previous": previous,
            "diff": diff,
            "diff_percent": diff_percent,
            "week_avg": week_avg,
            "trend": trend,
            "remaining": remaining,
            "progress": progress
        }
    
    def generate_advice(self, analysis: Dict) -> str:
        """「ダイエットの極意」に基づいたアドバイスを生成"""
        advice_lines = []
        
        advice_lines.append("## 🎯 今日の振り返りとアドバイス\n")
        advice_lines.append(f"**日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n")
        
        # 体重変化の評価
        latest = analysis["latest"]
        diff = analysis["diff"]
        
        advice_lines.append("### 📊 体重推移の分析\n")
        advice_lines.append(f"- **最新体重**: {latest.weight}kg")
        
        if diff < 0:
            advice_lines.append(f"- **前回比**: {diff:.1f}kg 減 ✨ 素晴らしい！")
            advice_lines.append(f"- 💪 **Good Job!** 身体が本来の機能を取り戻しつつあります！")
        elif diff > 0:
            advice_lines.append(f"- **前回比**: +{diff:.1f}kg")
            advice_lines.append(f"- 🌱 **大丈夫!** 体重は波があるもの。長期的なトレンドを見ましょう。")
        else:
            advice_lines.append(f"- **前回比**: 変化なし（安定）")
        
        advice_lines.append(f"- **週間平均**: {analysis['week_avg']:.1f}kg")
        advice_lines.append(f"- **傾向**: {analysis['trend']}")
        advice_lines.append(f"- **目標まで**: あと{analysis['remaining']:.1f}kg（達成率 {analysis['progress']:.1f}%）\n")
        
        # ダイエットの極意に基づいたアドバイス
        advice_lines.append("### 🧘‍♂️ 今日のアクションプラン\n")
        advice_lines.append("> 「失われた身体機能を呼び戻す」 - Ninniki-nene Style\n")
        
        # 体重に応じたアドバイス
        if diff >= 0.5:
            advice_lines.append("**📌 重点アクション**:")
            advice_lines.append("- ✅ 16時間断食を再確認（20時夕食→翌12時昼食）")
            advice_lines.append("- ✅ スワイショウ（腕振り運動）で代謝の地盤を作る")
            advice_lines.append("- ✅ 水分補給を意識（水、お茶、ブラックコーヒー）")
        elif diff < 0:
            advice_lines.append("**🌟 現在のリズムをキープ！**:")
            advice_lines.append("- ✅ 現在の食事リズムを継続")
            advice_lines.append("- ✅ 座りながらドローイン（お客様との通話中もOK）")
            advice_lines.append("- ✅ 1時間に1回、背骨リセット")
        else:
            advice_lines.append("**🔄 変化をつけてみましょう**:")
            advice_lines.append("- ✅ 運動のバリエーションを増やす（肩甲骨・股関節を動的に）")
            advice_lines.append("- ✅ 食事内容の見直し（添加物チェック）")
        
        advice_lines.append("\n**📝 今日の一言**:")
        advice_lines.append('> "10分あれば、座りながらでも機能は回復できる。今日も、本来の自分の身体機能を取り戻しましょう！"')
        
        return "\n".join(advice_lines)
    
    def update_record_file(self, advice: str):
        """記録.mdにアドバイスを追記"""
        content = self.record_file.read_text(encoding='utf-8')
        
        # 最新の日次記録セクションを探す
        latest = self.records[0]
        pattern = rf'(###\s+{latest.date}\s+\([^)]+\)\s+──[^\n]+)'
        
        match = re.search(pattern, content)
        if match:
            # その日の記録の後ろに追記
            insert_pos = match.end()
            
            # 既に振り返りが存在するかチェック
            next_section = content[insert_pos:insert_pos+500]
            if "## 🎯 今日の振り返りとアドバイス" in next_section:
                print("✅ 既に振り返りが存在します。上書きはしません。")
                return
            
            # 振り返りを挿入
            new_content = content[:insert_pos] + "\n\n" + advice + "\n" + content[insert_pos:]
            
            # バックアップを作成
            backup_file = self.record_file.with_suffix('.md.bak')
            backup_file.write_text(content, encoding='utf-8')
            print(f"📦 バックアップを作成: {backup_file}")
            
            # ファイルを更新
            self.record_file.write_text(new_content, encoding='utf-8')
            print(f"✅ 記録ファイルを更新しました: {self.record_file}")
        else:
            print(f"⚠️ 対象の日付セクションが見つかりませんでした: {latest.date}")

def main():
    """メイン実行関数"""
    print("🏥 ダイエット同期＆振り返りスクリプト起動\n")
    
    # ファイルパス設定
    script_dir = Path(__file__).parent
    record_file = script_dir / "記録.md"
    
    # アナライザー初期化
    analyzer = DietAnalyzer(record_file)
    
    # データ読み込み
    print("📖 体重記録を読み込み中...")
    records = analyzer.parse_records()
    
    if not records:
        print("❌ 体重データが見つかりませんでした。")
        return
    
    print(f"✅ {len(records)}件の記録を読み込みました。")
    print(f"   最新: {records[0]}\n")
    
    # 分析実行
    print("📊 体重推移を分析中...")
    analysis = analyzer.analyze_trend()
    
    if analysis.get("status") == "データ不足":
        print(f"⚠️ {analysis['message']}")
        return
    
    # アドバイス生成
    print("💡 アドバイスを生成中...\n")
    advice = analyzer.generate_advice(analysis)
    
    # 結果表示
    print("=" * 60)
    print(advice)
    print("=" * 60)
    
    # ファイル更新の確認
    print("\n📝 この内容を記録.mdに追記しますか？ (y/n): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        analyzer.update_record_file(advice)
        print("\n🎉 同期完了！ダイエット、頑張りましょう！")
    else:
        print("\n✋ 追記をキャンセルしました。")

if __name__ == "__main__":
    main()
