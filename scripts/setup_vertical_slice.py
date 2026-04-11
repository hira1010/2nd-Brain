import sys
import os

# scripts/lib へのパスを追加
current_dir = os.path.dirname(os.path.abspath(__file__))
rpg_dir = os.path.join(current_dir, '..', '05_RPG制作')
sys.path.append(os.path.join(rpg_dir, 'scripts', 'lib'))

from rpg_data import RpgMap
import json

def setup_map001():
    map_path = os.path.join(rpg_dir, 'data', 'Map001.json')
    try:
        rpg_map = RpgMap(map_path)
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    # 全イベントをクリーンアップ（真っ白にする）
    rpg_map.data['events'] = [None] 

    # 1. 宝箱（ドドド取得用） - セーフゾーン配置
    chest_event = {
        "id": 1,
        "name": "Chest_Dododo",
        "note": "",
        "pages": [
            {
                "conditions": {
                    "actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False,
                    "selfSwitchCh": "A", "selfSwitchValid": False,
                    "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                    "variableId": 1, "variableValid": False, "variableValue": 0
                },
                "directionFix": False,
                "image": {
                    "characterIndex": 5, "characterName": "!Chest", "direction": 2, "pattern": 0, "tileId": 0
                },
                "list": [
                    {"code": 250, "indent": 0, "parameters": [{"name": "Treasure1", "pan": 0, "pitch": 100, "volume": 90}]},
                    {"code": 205, "indent": 0, "parameters": [-1, {"list": [{"code": 17, "indent": None}, {"code": 0}], "repeat": False, "skippable": False, "wait": True}]},
                    {"code": 505, "indent": 0, "parameters": [{"code": 17, "indent": None}]},
                    {"code": 126, "indent": 0, "parameters": [39, 0, 0, 1]},
                    {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
                    {"code": 401, "indent": 0, "parameters": ["スキル『ドドド』を手に入れた！"]},
                    {"code": 123, "indent": 0, "parameters": ["A", 0]},
                    {"code": 0, "indent": 0, "parameters": []}
                ],
                "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "trigger": 0, "through": False, "walkAnime": True
            },
            {
                "conditions": {
                    "actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False,
                    "selfSwitchCh": "A", "selfSwitchValid": True,
                    "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                    "variableId": 1, "variableValid": False, "variableValue": 0
                },
                "directionFix": False,
                "image": {
                    "characterIndex": 5, "characterName": "!Chest", "direction": 8, "pattern": 0, "tileId": 0
                },
                "list": [{"code": 0, "indent": 0, "parameters": []}],
                "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "trigger": 0, "through": False, "walkAnime": True
            }
        ],
        "x": 2, "y": 2  # 左上の安全地帯
    }

    # 2. 突撃型敵（スライム）
    slime_event = {
        "id": 2,
        "name": "Enemy_Slime",
        "note": "<abs_enemy_id: 1>",
        "pages": [
            {
                "conditions": { "actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0 },
                "directionFix": False,
                "image": { "characterIndex": 0, "characterName": "Monster", "direction": 2, "pattern": 1, "tileId": 0 },
                "list": [{"code": 0, "indent": 0, "parameters": []}],
                "moveFrequency": 4, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 3, "moveType": 1, "priorityType": 1, "stepAnime": True, "trigger": 0, "through": False, "walkAnime": True
            }
        ],
        "x": 8, "y": 8
    }

    # 3. 射撃型敵（ゴースト）
    ghost_event = {
        "id": 3,
        "name": "Enemy_Ghost",
        "note": "<abs_enemy_id: 2>",
        "pages": [
            {
                "conditions": { "actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0 },
                "directionFix": False,
                "image": { "characterIndex": 4, "characterName": "Monster", "direction": 2, "pattern": 1, "tileId": 0 },
                "list": [{"code": 0, "indent": 0, "parameters": []}],
                "moveFrequency": 4, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 2, "moveType": 1, "priorityType": 1, "stepAnime": True, "trigger": 0, "through": True, "walkAnime": True
            }
        ],
        "x": 12, "y": 3
    }

    rpg_map.add_or_update_event(chest_event)
    rpg_map.add_or_update_event(slime_event)
    rpg_map.add_or_update_event(ghost_event)
    rpg_map.save()
    print("Map 001 safely rebuilt with core tutorial elements!")

if __name__ == '__main__':
    setup_map001()
