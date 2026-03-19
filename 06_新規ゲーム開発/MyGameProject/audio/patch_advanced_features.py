import json
import os

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data"

# 1. Weapons.json の更新
wp_path = os.path.join(base_dir, "Weapons.json")
with open(wp_path, "r", encoding="utf-8") as f:
    weapons = json.load(f)

# 新しい武器を追加
new_weapons = [
    {"id": 51, "animationId": 11, "description": "光り輝く音を放つ剣。", "etypeId": 1, "name": "ピカピカ剣", "note": "", "params": [0, 0, 20, 0, 0, 0, 0, 0], "price": 1000, "wtypeId": 1, "traits": []},
    {"id": 52, "animationId": 1, "description": "雷鳴のような音を放つ杖。", "etypeId": 1, "name": "ゴロゴロ杖", "note": "", "params": [0, 0, 5, 0, 30, 0, 0, 0], "price": 1200, "wtypeId": 6, "traits": []}
]

while len(weapons) <= 52:
    weapons.append(None)
weapons[51] = new_weapons[0]
weapons[52] = new_weapons[1]

with open(wp_path, "w", encoding="utf-8") as f:
    json.dump(weapons, f, ensure_ascii=False, separators=(',', ':'))

# 2. Items.json の更新
it_path = os.path.join(base_dir, "Items.json")
with open(it_path, "r", encoding="utf-8") as f:
    items = json.load(f)

items[2] = {"id": 2, "animationId": 0, "consumable": False, "description": "脱出に使用する鉄の鍵。", "itypeId": 1, "name": "脱出の鍵", "note": "", "occasion": 3, "price": 0, "repeats": 1, "scope": 0, "speed": 0, "successRate": 100, "tpGain": 0, "effects": []}
onomato_item = {"id": 3, "animationId": 0, "consumable": False, "description": "感情が結晶化したオノマトペの破片。", "itypeId": 1, "name": "オノマトペ of 破片", "name": "オノマトペの破片", "note": "", "occasion": 3, "price": 0, "repeats": 1, "scope": 0, "speed": 0, "successRate": 100, "tpGain": 0, "effects": []}
while len(items) <= 3:
    items.append(None)
items[3] = onomato_item

with open(it_path, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, separators=(',', ':'))

# 3. Troops.json の更新 (撃破演出と2P報酬)
tp_path = os.path.join(base_dir, "Troops.json")
with open(tp_path, "r", encoding="utf-8") as f:
    troops = json.load(f)

for troop in troops:
    if troop is None: continue
    event_page = {
        "conditions": {"actorHp": 50, "actorId": 1, "actorValid": False, "enemyHp": 0, "enemyIndex": 0, "enemyValid": True, "switchId": 1, "switchValid": False, "turnA": 0, "turnB": 0, "turnEnding": False, "turnValid": False},
        "list": [
            {"code": 250, "indent": 0, "parameters": [{"name": "Down1", "pan": 0, "pitch": 120, "volume": 90}]},
            {"code": 111, "indent": 0, "parameters": [4, 2]},
            {"code": 126, "indent": 1, "parameters": [3, 0, 0, 1]},
            {"code": 101, "indent": 1, "parameters": ["", 0, 0, 2, ""]},
            {"code": 401, "indent": 1, "parameters": ["2Pの活躍で【オノマトペの破片】を獲得！"]},
            {"code": 0, "indent": 1, "parameters": []},
            {"code": 412, "indent": 0, "parameters": []},
            {"code": 0, "indent": 0, "parameters": []}
        ],
        "span": 1
    }
    troop["pages"].append(event_page)

with open(tp_path, "w", encoding="utf-8") as f:
    json.dump(troops, f, ensure_ascii=False, separators=(',', ':'))

# 4. Map001.json への宝箱追加
map_path = os.path.join(base_dir, "Map001.json")
with open(map_path, "r", encoding="utf-8") as f:
    map_data = json.load(f)

if "events" not in map_data or map_data["events"] is None:
    map_data["events"] = [None]

chest_event = {
    "id": len(map_data["events"]),
    "name": "宝箱 (オノマトペ)",
    "note": "",
    "x": 8, "y": 8,
    "pages": [
        {
            "conditions": {"actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
            "image": {"characterIndex": 0, "characterName": "!Chest", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
                {"code": 401, "indent": 0, "parameters": ["宝箱を開けた！"]},
                {"code": 127, "indent": 0, "parameters": [51, 0, 0, 1, False]},
                {"code": 401, "indent": 0, "parameters": ["【ピカピカ剣】を手に入れた！"]},
                {"code": 123, "indent": 0, "parameters": ["A", 0]},
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}, "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": False
        },
        {
            "conditions": {"actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": True, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
            "image": {"characterIndex": 0, "characterName": "!Chest", "direction": 8, "pattern": 1, "tileId": 0},
            "list": [{"code": 0, "indent": 0, "parameters": []}],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}, "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": False
        }
    ]
}

map_data["events"].append(chest_event)

with open(map_path, "w", encoding="utf-8") as f:
    json.dump(map_data, f, ensure_ascii=False, separators=(',', ':'))

print("Advanced RPG features applied successfully.")
