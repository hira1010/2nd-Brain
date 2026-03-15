import json
import os

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\06_RPGゲーム成果物\data"

with open(os.path.join(base_dir, "Map002.json"), "r", encoding="utf-8") as f:
    map2 = json.load(f)

perfect_conditions = {
    "actorId": 1, "actorValid": False,
    "enemyIndex": 0, "enemyValid": False, 
    "itemId": 1, "itemValid": False,
    "selfSwitchCh": "A", "selfSwitchValid": False,
    "switch1Id": 1, "switch1Valid": False,
    "switch2Id": 1, "switch2Valid": False,
    "variableId": 1, "variableValid": False, "variableValue": 0
}

door_event = {
    "id": 1,
    "name": "扉 (出口)",
    "note": "",
    "x": 8, "y": 10,
    "pages": [
        {
            "conditions": perfect_conditions,
            "directionFix": True, # Keep the door looking like a door
            "image": {"characterIndex": 0, "characterName": "!Door1", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                # Conditional Branch: Item 5 (Escape Key) in inventory
                {"code": 111, "indent": 0, "parameters": [4, 5]},
                # - IF TRUE:
                {"code": 401, "indent": 1, "parameters": ["【脱出の鍵】を使った！扉が開いた！"]},
                {"code": 250, "indent": 1, "parameters": [{"name": "Open1", "pan": 0, "pitch": 100, "volume": 90}]},
                # Transfer to Map 1
                {"code": 201, "indent": 1, "parameters": [0, 1, 8, 10, 0, 0]},
                # - ELSE:
                {"code": 411, "indent": 0, "parameters": []},
                {"code": 401, "indent": 1, "parameters": ["鍵がかかっている……。脱出の鍵が必要だ。"]},
                {"code": 0, "indent": 1, "parameters": []},
                # END Cond
                {"code": 412, "indent": 0, "parameters": []},
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": False
        }
    ]
}

map2["events"][1] = door_event

with open(os.path.join(base_dir, "Map002.json"), "w", encoding="utf-8") as f:
    json.dump(map2, f, ensure_ascii=False, separators=(',', ':'))

# Update original too
try:
    with open(r"c:\Users\hirak\Desktop\2nd-Brain\25_RPGツクールフォルダ\data\Map002.json", "w", encoding="utf-8") as dst:
        json.dump(map2, dst, ensure_ascii=False, separators=(',', ':'))
except Exception:
    pass

print("Map002 door properly fixed with correct conditions.")
