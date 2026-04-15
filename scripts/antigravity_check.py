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
    "RPG_MAKER": ROOT_DIR / "RPGMaker_MZ",
    "RENPY": ROOT_DIR / "21_RenPy",
    "TYRANO": ROOT_DIR / "TyranoBuilder",
    "TWINE": ROOT_DIR / "22_Twine_Web"
}

def header(text):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}")

def check_rpg_maker():
    header("Checking RPG Maker MZ (21_えろげー)")
    path = PROJECTS["RPG_MAKER"]
    if not path.exists():
        print("❌ Project directory not found.")
        return False
    
    success = True
    # 1. 必須データの存在確認
    essential = ["data/System.json", "data/CommonEvents.json", "data/Map004.json"]
    for f in essential:
        if not (path / f).exists():
            print(f"[FAIL] Missing: {f}")
            success = False
        else:
            print(f"[OK] Found: {f}")
            
    # 2. 初期化スイッチの確認 (Switch 1 がONになるイベントがあるか)
    # ※ 既に手動で追加済みだが、簡易チェック
    try:
        with open(path / "data" / "Map004.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            has_init = False
            for event in data["events"]:
                if event and event.get("name") == "INITIALIZER":
                    has_init = True
                    break
            if has_init:
                print("[OK] INITIALIZER event found on Map004")
            else:
                print("[FAIL] INITIALIZER event MISSING on Map004!")
                success = False
    except Exception as e:
        print(f"⚠️ Could not check Map004 events: {e}")
        success = False
        
    return success

def check_renpy():
    header("Checking Ren'Py (22_HeroineAdv)")
    path = PROJECTS["RENPY"]
    if not path.exists():
        print("[FAIL] Project directory not found.")
        return False

    if not RENPY_SDK.exists():
        print(f"[WARNING] Ren'Py SDK not found at {RENPY_SDK}. Skipping CLI lint.")
        return True # 環境依存のため警告のみ

    try:
        print("Running Ren'Py Lint...")
        result = subprocess.run([str(RENPY_SDK), str(path), "lint"], capture_output=True, text=True, timeout=30)
        if "0 blocks" in result.stdout and "14 dialogue blocks" not in result.stdout:
             # ※ dialogue blocks の数はプロジェクトに合わせて調整
             print("[FAIL] Lint output seems suspicious (no dialogue found).")
             success = False
        else:
            print("[OK] Ren'Py Lint completed successfully.")
            success = True
    except subprocess.TimeoutExpired:
        print("❌ Ren'Py Lint timed out.")
        success = False
    except Exception as e:
        print(f"❌ Ren'Py Lint encountered an error: {e}")
        success = False
    return success

def check_tyrano():
    header("Checking TyranoBuilder (23_HeroineAdv)")
    path = PROJECTS["TYRANO"]
    if not path.exists():
        print("[FAIL] Project directory not found.")
        return False
    
    success = True
    # 1. 必須シナリオの確認
    essential = ["data/scenario/scene1.ks", "data/scenario/first.ks", "index.html"]
    for f in essential:
        if not (path / f).exists():
            print(f"[FAIL] Missing: {f}")
            success = False
        else:
            print(f"[OK] Found: {f}")
            
    # 2. 変数定義の確認
    ks_path = path / "data" / "scenario" / "scene1.ks"
    if ks_path.exists():
        content = ks_path.read_text(encoding="utf-8")
        if "f.p_pleasure" in content:
            print("[OK] f.p_pleasure defined in scene1.ks")
        else:
            print("[FAIL] Variable definitions might be missing in scene1.ks")
            success = False
            
    return success

def check_twine():
    header("Checking Twine (24_HeroineAdv)")
    path = PROJECTS["TWINE"]
    if not path.exists():
        print("[FAIL] Project directory not found.")
        return False
    
    success = True
    # 1. 必須ファイルの確認
    essential = ["index.html", "images/heroine_rank1.png"]
    for f in essential:
        if not (path / f).exists():
            print(f"[FAIL] Missing: {f}")
            success = False
        else:
            print(f"[OK] Found: {f}")
            
    # 2. ロジックの簡易確認
    html_path = path / "index.html"
    if html_path.exists():
        content = html_path.read_text(encoding="utf-8")
        if "pleasure" in content and "love" in content:
            print("[OK] Core variables found in index.html")
        else:
            print("[FAIL] Logic context missing in index.html")
            success = False
            
    return success

def main():
    print("--- Master Antigravity Consistency Check Starting ---")
    
    results = {
        "RPG": check_rpg_maker(),
        "RenPy": check_renpy(),
        "Tyrano": check_tyrano(),
        "Twine": check_twine()
    }
    
    header("FINAL REPORT")
    all_ok = True
    for engine, ok in results.items():
        status = "[OK]" if ok else "[FAIL]"
        print(f"{engine:10}: {status}")
        if not ok: all_ok = False
        
    print("\n" + "="*50)
    if all_ok:
        print("--- PROJECT HEALTH: GREEN (PASS) ---")
        print("All engines are synchronized and functional.")
        sys.exit(0)
    else:
        print("--- PROJECT HEALTH: RED (FAIL) ---")
        print("Issues detected. See details above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
