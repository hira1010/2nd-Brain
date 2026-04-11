import json
import os

MAP_PATH = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json'

def create_enemy_event(id, name, x, y, char_name, char_index, enemy_id):
    return {
        "id": id,
        "name": name,
        "x": x,
        "y": y,
        "note": f"<Enemy>\n<abs_enemy_id:{enemy_id}>",
        "pages": [{
            "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
            "directionFix": False,
            "image": {"characterIndex": char_index, "characterName": char_name, "direction": 2, "pattern": 1, "tileId": 0},
            "list": [{"code": 0, "indent": 0, "parameters": []}],
            "moveFrequency": 3, "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": True,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}
        }]
    }

def create_npc_event(id, name, x, y, char_name, char_index, dialog):
    event_list = []
    event_list.append({"code": 101, "indent": 0, "parameters": [char_name, char_index, 0, 2, "オノマトペの賢者"]})
    for line in dialog:
        event_list.append({"code": 401, "indent": 0, "parameters": [line]})
    event_list.append({"code": 0, "indent": 0, "parameters": []})

    return {
        "id": id,
        "name": name,
        "x": x,
        "y": y,
        "note": "",
        "pages": [{
            "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
            "directionFix": False,
            "image": {"characterIndex": char_index, "characterName": char_name, "direction": 2, "pattern": 1, "tileId": 0},
            "list": event_list,
            "moveFrequency": 3, "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": True,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}
        }]
    }

with open(MAP_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

current_ids = [e['id'] for e in data['events'] if e is not None]
next_id = max(current_ids) + 1 if current_ids else 1

# Add NPC
data['events'].append(create_npc_event(next_id, "賢者", 5, 5, "People1", 0, [
    "おお、レミよ。オノマトペの力を使いこなしておるか？",
    "PageUp/Downで武器を切り替え、OKボタンで放つが良い。",
    "盾(Aキー)を構えれば敵の攻撃を防げるぞ。",
    "敵を倒して『極意』を手に入れれば、威力も上がるはずじゃ。"
]))
next_id += 1

# Add Enemies
data['events'].append(create_enemy_event(next_id, "ゴブリン", 12, 5, "Monster", 2, 1))
next_id += 1
data['events'].append(create_enemy_event(next_id, "クロウ", 8, 8, "Monster", 1, 3))

with open(MAP_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully added 3 events to Map001.json")
