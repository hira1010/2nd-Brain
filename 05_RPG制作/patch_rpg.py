import json
import os

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data"

with open(os.path.join(base_dir, "Map002.json"), "r", encoding="utf-8") as f:
    map2 = json.load(f)

# The correct condition template based on Map001.json
base_condition = {
    "actorId": 1, "actorHp": 0, "enemyIndex": 0, "enemyHp": 0, "itemId": 1,
    "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, 
    "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0
}
base_condition_A_on = dict(base_condition)
base_condition_A_on["selfSwitchValid"] = True

door_event = {
    "id": 1, "name": "扉 (出口)", "note": "", "x": 8, "y": 12,
    "pages": [
        {
            "condition": base_condition,
            "directionFix": False, "image": {"characterIndex": 0, "characterName": "!Door1", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                {"code": 111, "indent": 0, "parameters": [4, 2, 0]}, # If Party has Item ID 2 (脱出の鍵)
                {"code": 401, "indent": 1, "parameters": ["【脱出の鍵】を使った！扉が開いた！"]},
                {"code": 250, "indent": 1, "parameters": [{"name": "Open1", "pan": 0, "pitch": 100, "volume": 90}]},
                {"code": 201, "indent": 1, "parameters": [0, 1, 8, 10, 0, 0]}, # Transfer to Map001
                {"code": 0, "indent": 1, "parameters": []},
                {"code": 411, "indent": 0, "parameters": []}, # Else
                {"code": 401, "indent": 1, "parameters": ["鍵がかかっている……。脱出の鍵が必要だ。"]},
                {"code": 0, "indent": 1, "parameters": []},
                {"code": 412, "indent": 0, "parameters": []}, # Branch end
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": False
        }
    ]
}

chest_event = {
    "id": 2, "name": "隠された鍵", "note": "", "x": 3, "y": 3,
    "pages": [
        {
            "condition": base_condition,
            "directionFix": False, "image": {"characterIndex": 0, "characterName": "!Chest", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
                {"code": 401, "indent": 0, "parameters": ["宝箱の中に【脱出の鍵】を見つけた！"]},
                {"code": 126, "indent": 0, "parameters": [2, 0, 0, 1]}, # Get Item ID 2
                {"code": 123, "indent": 0, "parameters": ["A", 0]}, # Self Switch A ON
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": False
        },
        {
            "condition": base_condition_A_on,
            "directionFix": False, "image": {"characterIndex": 0, "characterName": "!Chest", "direction": 8, "pattern": 1, "tileId": 0},
            "list": [{"code": 0, "indent": 0, "parameters": []}],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": False
        }
    ]
}

fake_event = {
    "id": 3, "name": "ガレキ", "note": "", "x": 13, "y": 5,
    "pages": [
        {
            "condition": base_condition,
            "directionFix": False, "image": {"characterIndex": 0, "characterName": "!Flame", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
                {"code": 401, "indent": 0, "parameters": ["炎が燃えている……。ここには何もなさそうだ。"]},
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": True, "through": False, "trigger": 0, "walkAnime": False
        }
    ]
}

map2["events"] = [None, door_event, chest_event, fake_event]

# Save back to JSON
with open(os.path.join(base_dir, "Map002.json"), "w", encoding="utf-8") as f:
    json.dump(map2, f, separators=(',', ':'), ensure_ascii=False)

print("Modification complete.")
