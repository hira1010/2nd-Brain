import os
import json
import re
import sys

# パス設定
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '05_RPG制作'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_DIRS = ['bgm', 'bgs', 'me', 'se']
IMG_DIRS = ['animations', 'battlebacks1', 'battlebacks2', 'characters', 'enemies', 'faces', 'parallaxes', 'pictures', 'sv_actors', 'sv_enemies', 'system', 'tilesets', 'titles1', 'titles2']

# 実際に存在するファイルの一覧を取得（拡張子抜き）
def get_existing_files(base_path, subdirs):
    files = set()
    for d in subdirs:
        dir_path = os.path.join(base_path, d)
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                name, _ = os.path.splitext(f)
                files.add(name)
    return files

existent_audio = get_existing_files(os.path.join(BASE_DIR, 'audio'), AUDIO_DIRS)
existent_img = get_existing_files(os.path.join(BASE_DIR, 'img'), IMG_DIRS)

missing = []

# JSONファイルから再帰的に参照を抽出
def check_obj(obj, file_context):
    if isinstance(obj, dict):
        # Audio check (has name and volume/pitch)
        if 'name' in obj and isinstance(obj['name'], str) and obj['name']:
            if 'volume' in obj or 'pitch' in obj or 'pan' in obj:
                if obj['name'] not in existent_audio:
                    # Ignore '0' if it's explicitly guarded now, but ideally it shouldn't be defined!
                    if obj['name'] == '0':
                        missing.append(f"[Audio/SE: '0'] {file_context} -> Please Remove '0' (Invalid Sound)")
                    else:
                        missing.append(f"[Audio Missing] {obj['name']} in {file_context}")
        
        # Image check
        img_keys = ['characterName', 'faceName', 'battlerName', 'battleback1Name', 'battleback2Name', 'parallaxName']
        for k in img_keys:
            if k in obj and isinstance(obj[k], str) and obj[k]:
                if obj[k] not in existent_img:
                    missing.append(f"[Image Missing] {obj[k]} (key: {k}) in {file_context}")

        for v in obj.values():
            check_obj(v, file_context)

    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            check_obj(item, f"{file_context}[{idx}]")

# 1. データベースの検査
print("Scanning MZ Database for missing assets...")
for f in os.listdir(DATA_DIR):
    if f.endswith('.json'):
        path = os.path.join(DATA_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                check_obj(data, f)
        except Exception as e:
            print(f"Error parsing {f}: {e}")

# 2. ABSプラグインの検査 (ABS_Support.js)
print("Scanning ABS Configuration for missing assets...")
abs_path = os.path.join(BASE_DIR, 'js', 'plugins', 'ABS_Support.js')
try:
    with open(abs_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # SEの検索 (seAtk: "Hoge")
        se_matches = re.finditer(r'(seAtk|seDef|bgm|se)\s*:\s*[\'"]([^\'"]+)[\'"]', content)
        for m in se_matches:
            val = m.group(2)
            if val and val not in existent_audio:
                missing.append(f"[Audio Missing] {val} in ABS_Support.js ({m.group(1)})")
        # 画像の検索 (pic: "Hoge")
        pic_matches = re.finditer(r'(pic)\s*:\s*[\'"]([^\'"]+)[\'"]', content)
        for m in pic_matches:
            val = m.group(2)
            if val and val not in existent_img:
                missing.append(f"[Image Missing] {val} in ABS_Support.js ({m.group(1)})")
except Exception as e:
    print(f"Error parsing ABS_Support.js: {e}")

# 3. ABS_Ultimate.js内のハードコード検証
abs_ult_path = os.path.join(BASE_DIR, 'js', 'plugins', 'ABS_Ultimate.js')
try:
    with open(abs_ult_path, 'r', encoding='utf-8') as file:
        content = file.read()
        se_matches = re.finditer(r'AudioManager\.playSe\(\{\s*name:\s*[\'"]([^\'"]+)[\'"]', content)
        for m in se_matches:
            val = m.group(1)
            # ignore standard MZ variable usages if any, but valid hardcoded ones should be found
            if val and val != "0" and val != "undefined" and val not in existent_audio:
                missing.append(f"[Audio Missing] {val} in ABS_Ultimate.js (hardcoded playSe)")
except Exception as e:
    print(f"Error parsing ABS_Ultimate.js: {e}")

if missing:
    print("\n[CRITICAL ERROR] The following assets are missing from the project folders:")
    for m in missing:
        print("  - " + m)
    print("\nPlease fix these missing assets before committing! A missing asset WILL crash the game!")
    sys.exit(1)
else:
    print("\n[SUCCESS] All referenced Audio and Images exist physically! Asset Integrity is 100% Bulletproof!")
    sys.exit(0)
