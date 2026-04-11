import json
import os
import random

# パスの設定
DATA_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data"

# ステージ設定
STAGES = {
    1: {"name": "1. 欲望の平原", "bgm": "Field1", "tint": [0, 0, 0, 0]},
    2: {"name": "2. 蜜の滴る大森林", "bgm": "Ship3", "tint": [-34, 0, -34, 34]},
    8: {"name": "3. 情熱の灼熱火山", "bgm": "Dungeon1", "tint": [60, -30, -60, 60]},
    5: {"name": "4. 凍える吐息の氷穴", "bgm": "Dungeon2", "tint": [-60, -30, 60, 60]},
    4: {"name": "5. 背徳の地下迷宮", "bgm": "Dungeon3", "tint": [-100, -100, -100, 150]},
    7: {"name": "6. 桃源郷の空中庭園", "bgm": "Field2", "tint": [30, 30, 60, 0]},
    6: {"name": "7. 淫欲の魔王宮", "bgm": "Theme4", "tint": [40, -40, -40, 80]}
}

# ステージ進行順
SEQUENCE = [1, 2, 8, 5, 4, 7, 6]

def backup_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
        with open(filepath + ".bak_enhancer", 'w', encoding='utf-8') as f:
            f.write(data)

def enhance_map(map_id, config):
    filename = f"Map{map_id:03d}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"Skipping {filename}: File not found.")
        return

    print(f"Enhancing {filename} ({config['name']})...")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        map_data = json.load(f)

    # 1. 基本設定の更新
    map_data["displayName"] = config["name"]
    map_data["bgm"]["name"] = config["bgm"]
    map_data["autoplayBgm"] = True

    # 2. 地形デコレーション (Layer 3: 装飾)
    # dataは [Layer0...Layer5] のフラットな配列。要素数は width * height * 6
    width = map_data["width"]
    height = map_data["height"]
    layer_size = width * height
    
    # 装飾タイルの選定 (Tile B想定)
    # 自然系 (1, 2, 8, 5, 7) と 建物系 (4, 6)
    decor_tiles = [16, 17, 18, 32, 33, 34] if map_id in [1, 2, 8, 5, 7] else [192, 193, 200, 201]

    # Layer 3 にランダムに装飾を散らす
    for y in range(height):
        for x in range(width):
            idx = 3 * layer_size + (y * width + x)
            # 現在のタイルが空(0)の場合のみ、低確率で装飾を置く
            if map_data["data"][idx] == 0 and random.random() < 0.08:
                map_data["data"][idx] = random.choice(decor_tiles)

    # 3. 環境演出イベントの注入 (平行処理イベント)
    # 既存の演出イベントをクリアするか、追加する
    tint = config["tint"]
    tint_event = {
        "id": len(map_data["events"]) + 1,
        "name": "Env_Tint",
        "note": "",
        "pages": [{
            "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
            "directionFix": False,
            "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 0, "tileId": 0},
            "list": [
                {"code": 223, "indent": 0, "parameters": [tint, 60, True]}, # 色調変更
                {"code": 214, "indent": 0, "parameters": []}, # 画面の消去(演出リセット等)
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 0,
            "stepAnime": False,
            "through": False,
            "trigger": 3, # 並列処理
            "walkAnime": True
        }],
        "x": 0,
        "y": 0
    }
    map_data["events"].append(tint_event)

    # 4. 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)

def update_map_infos():
    filepath = os.path.join(DATA_DIR, "MapInfos.json")
    if not os.path.exists(filepath):
        return
    
    backup_file(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        infos = json.load(f)

    for info in infos:
        if info and info["id"] in STAGES:
            info["name"] = STAGES[info["id"]]["name"]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(infos, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_map_infos()
    for map_id, config in STAGES.items():
        enhance_map(map_id, config)
    print("Map enhancement complete!")
