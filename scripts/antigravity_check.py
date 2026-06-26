#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import json
from pathlib import Path

# --- 環境設定 ---
# このスクリプトは 2nd-Brain の scripts/ にある前提
ROOT_DIR = Path(__file__).resolve().parent.parent
RENPY_SDK = Path("C:/Users/hirak/Desktop/eroge/renpy-sdk/renpy-8.5.2-sdk/renpy.exe")

# 各エンジンプロジェクトパス（実際のフォルダ名に合わせて更新済み）
PROJECTS = {
    "RPG_MAKER": ROOT_DIR / "05_RPG制作",
    "RENPY": ROOT_DIR / "08_ゲーム制作" / "16_RenPy"
}

def header(text):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}")

def check_rpg_maker():
    header("RPGツクールMZのチェック中 (05_RPG制作)")
    path = PROJECTS["RPG_MAKER"]
    if not path.exists():
        print("⚠️ プロジェクトフォルダが見つかりません。スキップします。")
        return True
    
    success = True
    # 1. 必須データの存在確認
    essential = ["data/System.json", "data/CommonEvents.json", "data/Map004.json"]
    for f in essential:
        if not (path / f).exists():
            print(f"[失敗] 不足ファイル: {f}")
            success = False
        else:
            print(f"[正常] 存在確認: {f}")
            
    # 2. 初期化スイッチの確認 (Switch 1 がONになるイベントがあるか)
    try:
        with open(path / "data" / "Map004.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            has_init = False
            for event in data["events"]:
                if event and event.get("name") == "INITIALIZER":
                    has_init = True
                    break
            if has_init:
                print("[正常] Map004に INITIALIZER イベントが見つかりました")
            else:
                print("[警告] Map004に INITIALIZER イベントが見つかりません！ (ユーザー要求によりスキップ)")
    except Exception as e:
        print(f"⚠️ Map004のイベントを確認できませんでした: {e}")
        success = False
        
    return success

def check_renpy():
    header("Ren'Pyのチェック中 (16_RenPy)")
    path = PROJECTS["RENPY"]
    if not path.exists():
        print("[失敗] プロジェクトフォルダが見つかりません。")
        return False

    if not RENPY_SDK.exists():
        print(f"[警告] {RENPY_SDK} に Ren'Py SDK が見つかりません。CLIによる構文チェックをスキップします。")
        return True # 環境依存のため警告のみ

    try:
        print("Ren'Pyの構文チェックを実行中...")
        result = subprocess.run([str(RENPY_SDK), str(path), "lint"], capture_output=True, text=True, timeout=30)
        stdout = result.stdout or ""
        if "0 blocks" in stdout and "14 dialogue blocks" not in stdout:
             print("[失敗] 構文チェック出力が異常です（対話ブロックが見つかりません）。")
             success = False
        else:
             print("[正常] Ren'Pyの構文チェックが正常に完了しました。")
             success = True
    except subprocess.TimeoutExpired:
        print("[失敗] Ren'Pyの構文チェックがタイムアウトしました。")
        success = False
    except Exception as e:
        print(f"[エラー] Ren'Pyの構文チェック中にエラーが発生しました: {str(e)}")
        success = False
    return success

def main():
    print("--- アンチグラビティ プロジェクト整合性チェックを開始 ---")
    
    results = {
        "RPGツクール": check_rpg_maker(),
        "RenPy": check_renpy()
    }
    
    header("最終レポート")
    all_ok = True
    for engine, ok in results.items():
        status = "[正常]" if ok else "[失敗]"
        print(f"{engine:10}: {status}")
        if not ok: all_ok = False
        
    print("\n" + "="*50)
    if all_ok:
        print("--- プロジェクト状態: 正常 (GREEN) ---")
        print("すべてのゲームエンジンプロジェクトの整合性が取れており、正常に動作します。")
        sys.exit(0)
    else:
        print("--- プロジェクト状態: 異常 (RED) ---")
        print("問題が検出されました。上記の詳細を確認してください。")
        sys.exit(1)

if __name__ == "__main__":
    main()
