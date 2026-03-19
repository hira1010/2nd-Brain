import json, shutil

# Map001に洞窟の入り口イベントを追加する
path1 = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json'
shutil.copy(path1, path1 + '.bak2')

with open(path1, 'r', encoding='utf-8') as f:
    m1 = json.load(f)

# 既存イベント最大IDを取得
existing_ids = [e['id'] for e in m1['events'] if e]
next_id = max(existing_ids) + 1 if existing_ids else 1

# 洞窟入り口イベント（場所移動 → Map002のx=8, y=1付近に出現）
cave_entrance = {
    "id": next_id,
    "name": "洞窟の入り口",
    "note": "",
    "x": 8,
    "y": 3,
    "pages": [
        {
            "conditions": {
                "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False,
                "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                "variableId": 1, "variableValid": False, "variableValue": 0
            },
            "directionFix": True,
            "image": {
                "characterIndex": 0,
                "characterName": "!Door1",
                "direction": 2,
                "pattern": 1,
                "tileId": 0
            },
            "list": [
                # 場所移動コマンド: mapId=2, x=8, y=8
                {"code": 201, "indent": 0, "parameters": [0, 2, 8, 8, 0, 0]},
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3,
            "moveRoute": {
                "list": [{"code": 0, "parameters": []}],
                "repeat": True, "skippable": False, "wait": False
            },
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 1,
            "stepAnime": False,
            "through": False,
            "trigger": 0,  # 決定キーで反応
            "walkAnime": False
        }
    ]
}

m1['events'].append(cave_entrance)

with open(path1, 'w', encoding='utf-8', newline='') as f:
    json.dump(m1, f, ensure_ascii=False, separators=(',', ':'))

print("Map001に洞窟の入り口を追加しました！")
print(f"  イベント位置: x=8, y=3 (前にプレイヤーが立って決定キーで洞窟に入る)")
print(f"  移動先: Map002 (x=8, y=8)")
print(f"  イベント一覧:")
for e in m1['events']:
    if e:
        print(f"    ID={e['id']} name={e['name']} pos=({e['x']},{e['y']})")

# Map002のencounterListも改めて確認
print()
m2 = json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json', encoding='utf-8'))
print(f"Map002 encounterList: {m2['encounterList']}")
print(f"Map002 encounterStep: {m2['encounterStep']}")
