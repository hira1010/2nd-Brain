import json, shutil

# ============================================================
# Map002: バトルバック修正 + オノマトペ武器イベント追加
# Map001: オノマトペ武器イベント追加（ドカバキハンマー）
# ============================================================

# バトルバックのファイル確認
import os
bb_dir = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\img\battlebacks1'
if os.path.exists(bb_dir):
    files = os.listdir(bb_dir)
    cave_files = [f for f in files if 'cave' in f.lower() or 'Cave' in f]
    print(f"洞窟系バトルバック: {cave_files[:10]}")
    print(f"全ファイル: {files[:20]}")
else:
    print("battlebacks1フォルダが見つかりません")

# Map002修正
path2 = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json'
shutil.copy(path2, path2 + '.bak2')
with open(path2, 'r', encoding='utf-8') as f:
    m2 = json.load(f)

# バトルバックを空に戻す（存在しないファイルを指定しているとエラーになる可能性）
m2['battleback1Name'] = ''
m2['battleback2Name'] = ''
m2['specifyBattleback'] = False

# Map002にオノマトペ武器イベントを追加
# 既存イベントの最大IDを取得
existing_ids = [e['id'] for e in m2['events'] if e]
next_id = max(existing_ids) + 1

# ピカピカ剣はすでにMap001にある。Map002にゴロゴロ杖イベントを追加
def make_weapon_event(event_id, name, weapon_id, x, y):
    """武器を拾えるイベントを作成"""
    return {
        "id": event_id,
        "name": f"武器 ({name})",
        "note": "",
        "x": x,
        "y": y,
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
                    "characterIndex": 0,
                    "characterName": "!Chest",
                    "direction": 2,
                    "pattern": 1,
                    "tileId": 0
                },
                "list": [
                    {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
                    {"code": 401, "indent": 0, "parameters": [f"【{name}】が落ちていた！"]},
                    {"code": 127, "indent": 0, "parameters": [weapon_id, 0, 0, 1, False]},
                    {"code": 401, "indent": 0, "parameters": [f"【{name}】を手に入れた！"]},
                    {"code": 123, "indent": 0, "parameters": ["A", 0]},
                    {"code": 0, "indent": 0, "parameters": []}
                ],
                "moveFrequency": 3,
                "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 3,
                "moveType": 0,
                "priorityType": 1,
                "stepAnime": False,
                "through": False,
                "trigger": 0,
                "walkAnime": False
            },
            {
                # セルフスイッチA=ONの場合（拾った後）は空
                "conditions": {
                    "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                    "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": True,
                    "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                    "variableId": 1, "variableValid": False, "variableValue": 0
                },
                "directionFix": False,
                "image": {
                    "characterIndex": 0,
                    "characterName": "!Chest",
                    "direction": 8,
                    "pattern": 1,
                    "tileId": 0
                },
                "list": [{"code": 0, "indent": 0, "parameters": []}],
                "moveFrequency": 3,
                "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                "moveSpeed": 3,
                "moveType": 0,
                "priorityType": 1,
                "stepAnime": False,
                "through": False,
                "trigger": 0,
                "walkAnime": False
            }
        ]
    }

# Map002にオノマトペ武器2つを追加
# ゴロゴロ杖(ID=52)は位置(5,5)、ドカバキハンマー(ID=1)は位置(12,5)
m2['events'].append(make_weapon_event(next_id, 'ゴロゴロ杖', 52, 5, 5))
m2['events'].append(make_weapon_event(next_id + 1, 'ドカバキハンマー', 1, 12, 8))

with open(path2, 'w', encoding='utf-8', newline='') as f:
    json.dump(m2, f, ensure_ascii=False, separators=(',', ':'))
print("Map002.json修正完了！")
print(f"  tilesetId={m2['tilesetId']} (4=Dungeon)")
print(f"  encounterList={m2['encounterList']}")
print(f"  イベント数={len([e for e in m2['events'] if e])}")

# Map001にシュバシュバ刀(ID=2)のイベントを追加
path1 = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json'
shutil.copy(path1, path1 + '.bak')
with open(path1, 'r', encoding='utf-8') as f:
    m1 = json.load(f)

existing_ids1 = [e['id'] for e in m1['events'] if e]
next_id1 = max(existing_ids1) + 1 if existing_ids1 else 1

m1['events'].append(make_weapon_event(next_id1, 'シュバシュバ刀', 2, 4, 4))

with open(path1, 'w', encoding='utf-8', newline='') as f:
    json.dump(m1, f, ensure_ascii=False, separators=(',', ':'))
print("Map001.json修正完了！")
print(f"  イベント数={len([e for e in m1['events'] if e])}")
