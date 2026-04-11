#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from pathlib import Path

# プロジェクトルートの設定
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from lib import utils
utils.initialize_script("antigravity_check")

RPG_DIR = ROOT_DIR / "05_RPG制作"
PLUGINS_DIR = RPG_DIR / "js" / "plugins"
TESTS_DIR = RPG_DIR / "tests"

def check_js_syntax():
    """js/plugins 内の全ファイルおよび js/plugins.js の構文チェックを行う"""
    print("--- [1/3] Plugin Syntax Check ---")
    
    # チェック対象リスト
    targets = list(PLUGINS_DIR.glob("*.js"))
    targets.append(RPG_DIR / "js" / "plugins.js")
    
    success = True
    for js_file in targets:
        if not js_file.exists(): continue
        try:
            # node --check で構文チェック
            result = subprocess.run(["node", "--check", str(js_file)], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Syntax Error in {js_file.name}:")
                print(result.stderr)
                success = False
            else:
                # 特別なテスト: plugins.js 内で $plugins が定義されているか
                if js_file.name == "plugins.js":
                    content = js_file.read_text(encoding="utf-8")
                    if "var $plugins =" not in content and "var $plugins=" not in content:
                        print("❌ CRITICAL: '$plugins' variable is missing in plugins.js!")
                        success = False
                    else:
                        print(f"✅ {js_file.name}: Syntax & $plugins OK")
                else:
                    print(f"✅ {js_file.name}: Syntax OK")
        except Exception as e:
            print(f"⚠️ Failed to check {js_file.name}: {e}")
    return success

def run_virtual_tests():
    """RPG Maker 仮想環境でのテスト実行"""
    print("\n--- [2/3] RPG Maker Virtual Test ---")
    test_script = TESTS_DIR / "check_plugin.js"
    if not test_script.exists():
        print("⚠️ Test script not found. Skipping.")
        return True
    
    result = subprocess.run(["node", str(test_script)], cwd=str(RPG_DIR), capture_output=True, text=True, encoding="utf-8")
    if result.returncode == 0:
        print("✅ Virtual Test Passed!")
        return True
    else:
        print("❌ Virtual Test FAILED!")
        if result.stdout: print(result.stdout)
        if result.stderr: print(result.stderr)
        return False

def check_plugin_existence():
    """plugins.js に登録されている全ファイルが実際にディスク上に存在するか確認する"""
    print("\n--- [1.5/3] Plugin Existence Check ---")
    p_js = RPG_DIR / "js" / "plugins.js"
    if not p_js.exists():
        print("❌ plugins.js not found!")
        return False
    
    content = p_js.read_text(encoding="utf-8")
    # 簡易パース: {"name":"xxx",...} の形式を探す
    import re
    # name属性を抽出
    names = re.findall(r'\"name\"\s*:\s*\"(.*?)\"', content)
    
    success = True
    for name in names:
        filename = f"{name}.js"
        path = PLUGINS_DIR / filename
        if not path.exists():
            print(f"❌ REGISTERED BUT MISSING: {filename}")
            success = False
        else:
            print(f"✅ Found: {filename}")
    return success

def check_essential_files():
    """必須データの存在確認"""
    print("\n--- [3/3] Essential Data Consistency Check ---")
    needed = ["data/Actors.json", "data/System.json", "data/Map001.json", "js/plugins.js"]
    success = True
    for f in needed:
        p = RPG_DIR / f
        if not p.exists():
            print(f"❌ Missing critical file: {f}")
            success = False
        else:
            print(f"✅ Found: {f}")
    return success

def check_image_assets():
    """キャラクター画像の規格チェック (サイズ、透過など)"""
    print("\n--- [2.5/3] Image Asset Validation ---")
    try:
        from PIL import Image
    except ImportError:
        print("⚠️ Pillow not installed. Skipping image check.")
        return True
    
    char_dir = RPG_DIR / "img" / "characters"
    if not char_dir.exists(): return True
    
    success = True
    for img_file in char_dir.glob("*.png"):
        try:
            with Image.open(img_file) as img:
                # 1. $プレフィックス (シングルシート) のチェック
                if img_file.name.startswith("$"):
                    w, h = img.size
                    if w % 3 != 0 or h % 4 != 0:
                        print(f"❌ INVALID SIZE for Single Sheet: {img_file.name} ({w}x{h})")
                        print("   -> Width must be multiple of 3, Height multiple of 4.")
                        success = False
                    else:
                        print(f"✅ {img_file.name}: Tile Size OK ({w // 3}x{h // 4})")
                
                # 2. 透過チェック (AI特有の格子模様の検出)
                # 簡易的に隅が不透明な灰色系かを判定
                if img.mode == "RGBA":
                    pix = img.getpixel((0, 0))
                    if pix[3] > 200 and pix[0] > 150 and pix[1] > 150 and abs(pix[0]-pix[1]) < 10:
                        print(f"❌ SUSPECTED FAKE TRANSPARENCY: {img_file.name}")
                        print("   -> Corner is opaque gray/white. (Checkerboard?)")
                        success = False
        except Exception as e:
            print(f"⚠️ Failed to open {img_file.name}: {e}")
            
    return success

def main():
    print("========================================")
    print("   Antigravity Self-Quality Guard")
    print("========================================\n")
    
    s1 = check_js_syntax()
    s_exist = check_plugin_existence()
    s2 = run_virtual_tests()
    s_img = check_image_assets() # NEW
    s3 = check_essential_files()
    
    print("\n========================================")
    if s1 and s_exist and s2 and s_img and s3:
        print("🛡️  PROJECT HEALTH: GREEN (✅)")
        print("Antigravity is allowed to report 'Done'.")
        sys.exit(0)
    else:
        print("🚨 PROJECT HEALTH: RED (❌)")
        print("Antigravity MUST fix issues before reporting 'Done'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
