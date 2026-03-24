import json
import os

path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json'

def create_event(id, name, x, y, list_commands, move_type=0, character_name="", character_index=0, note="", trigger=0, move_frequency=3):
    return {
        "id": id,
        "name": name,
        "note": note,
        "pages": [
            {
                "conditions": {
                    "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                    "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False,
                    "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                    "variableId": 1, "variableValid": False, "variableValue": 0
                },
                "directionFix": False,
                "image": {
                    "characterIndex": character_index,
                    "characterName": character_name,
                    "direction": 2,
                    "pattern": 1,
                    "tileId": 0
                },
                "list": list_commands + [{"code": 0, "indent": 0, "parameters": []}],
                "moveFrequency": move_frequency,
                "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 3,
                "moveType": move_type,
                "priorityType": 1,
                "stepAnime": False,
                "through": False,
                "trigger": trigger,
                "walkAnime": True
            }
        ],
        "x": x,
        "y": y
    }

def get_item_commands(item_id, item_name):
    return [
        {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
        {"code": 401, "indent": 0, "parameters": ["宝箱を開けた！"]},
        {"code": 224, "indent": 0, "parameters": [[255, 255, 255, 128], 60, True]},
        {"code": 250, "indent": 0, "parameters": [{"name": "Powerup", "volume": 90, "pitch": 100, "pan": 0}]},
        {"code": 127, "indent": 0, "parameters": [item_id, 0, 0, 1, False]},
        {"code": 401, "indent": 0, "parameters": [f"【{item_name}】を手に入れた！"]},
        {"code": 123, "indent": 0, "parameters": ["A", 0]}
    ]

data = [2816] * (17 * 13) + [0] * (17 * 13 * 5)
events = [None]

# ID 1
events.append(create_event(1, "宝箱 (オノマトペ)", 8, 8, get_item_commands(51, "ピカピカ剣"), character_name="!Chest"))
# ID 2
events.append(create_event(2, "武器 (シュバシュバ刀)", 4, 4, get_item_commands(2, "シュバシュバ刀"), character_name="!Chest"))
# ID 3-9
for i in range(3, 10):
    events.append(create_event(i, f"Event {i}", 0, 0, []))

# ID 10 (Startup - Opening sequence "Instant Movie" version)
opening_list = [
    {"code": 221, "indent": 0, "parameters": []}, # Fadeout
    {"code": 223, "indent": 0, "parameters": [[-128, -128, -128, 0], 0, True]}, # Tint to Dark
    {"code": 355, "indent": 0, "parameters": ["Video.play('movies/0320.webm');"]}, # Start Movie via Script (Non-blocking)
    {"code": 101, "indent": 0, "parameters": ["", 0, 1, 1, ""]}, # Top, transparent
    {"code": 401, "indent": 0, "parameters": ["この世には７つのオノマトペがある。"]},
    {"code": 401, "indent": 0, "parameters": ["それをそろえたとき、最高の美女動画がみれるという……。"]},
    {"code": 230, "indent": 0, "parameters": [30]}, # Wait 30 frames (0.5s)
    {"code": 355, "indent": 0, "parameters": ["Video._element.pause(); Video._element.style.display = 'none';"]}, # Instant Stop
    {"code": 223, "indent": 0, "parameters": [[0, 0, 0, 0], 30, True]}, # Reset Tint
    {"code": 222, "indent": 0, "parameters": []}, # Fadein
    {"code": 121, "indent": 0, "parameters": [1, 1, 0]}, # Switch 1 ON
    {"code": 127, "indent": 0, "parameters": [51, 0, 0, 1, False]},
    {"code": 122, "indent": 0, "parameters": [5, 5, 0, 0, 0]},
    {"code": 214, "indent": 0, "parameters": []}
]
e10 = create_event(10, "Startup", 0, 0, opening_list)
e10["pages"][0]["trigger"] = 3
e10["pages"][0]["through"] = True
events.append(e10)

# Enemy attack list
enemy_attack_list = [
    {"code": 212, "indent": 0, "parameters": [-1, 1, True]}, 
    {"code": 311, "indent": 0, "parameters": [0, 0, 0, 5, False]}, 
    {"code": 250, "indent": 0, "parameters": [{"name": "Blow1", "volume": 90, "pitch": 100, "pan": 0}]},
    {"code": 105, "indent": 0, "parameters": [30, False]}
]

# ID 11 & Others
events.append(create_event(11, "Enemy", 5, 5, enemy_attack_list, move_type=3, character_name="Monster", character_index=0, note="<Enemy>", trigger=1, move_frequency=5))
for i, name, item in [(12, "ドドド", 32), (13, "ドキドキ", 33), (14, "ふわっ", 34), (15, "ちゅちゅ", 35), (16, "きゅん", 36), (17, "わくわく", 37)]:
    events.append(create_event(i, f"宝箱 ({name})", 10+(i-12)*2 if i<16 else 2+(i-16)*2, 10, get_item_commands(item, f"{name}の極意"), character_name="!Chest", character_index=0))
coords = [(3, 7), (7, 5), (12, 3), (15, 8), (9, 2), (2, 11), (10, 11), (14, 2), (1, 1), (15, 12), (8, 12), (16, 6)]
for i, (ex, ey) in enumerate(coords, 18):
    events.append(create_event(i, "Enemy", ex, ey, enemy_attack_list, move_type=3, character_name="Monster", character_index=(i-18)%8, note="<Enemy>", trigger=1, move_frequency=5))

map_obj = {
    "autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "",
    "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
    "disableDashing": False, "displayName": "", "encounterList": [], "encounterStep": 30,
    "height": 13, "note": "", "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": "",
    "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0, "specifyBattleback": False,
    "tilesetId": 1, "width": 17, "data": data, "events": events
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(map_obj, f, ensure_ascii=False, indent=2)

print("Map001.json opening adjusted to 'Instant Movie' mode.")
