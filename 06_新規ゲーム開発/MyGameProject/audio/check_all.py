import json

# 全タイルセット確認
ts = json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Tilesets.json', encoding='utf-8'))
print("=== タイルセット一覧 ===")
for t in ts:
    if t:
        print(f'ID={t["id"]} name={t["name"]}')

# 開始マップ確認
sys_data = json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\System.json', encoding='utf-8'))
print(f"\n=== スタート情報 ===")
print(f'startMapId={sys_data.get("startMapId")} x={sys_data.get("startX")} y={sys_data.get("startY")}')

# Map002のencounterList確認
m2 = json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json', encoding='utf-8'))
print(f"\n=== Map002 ===")
print(f'tilesetId={m2["tilesetId"]}')
print(f'encounterList={m2["encounterList"]}')
print(f'events = {[e.get("name","") for e in m2["events"] if e]}')

# Map001のencounterList確認
map1 = json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json', encoding='utf-8'))
print(f"\n=== Map001 ===")
print(f'tilesetId={map1["tilesetId"]}')
print(f'encounterList={map1["encounterList"]}')
print(f'events = {[e.get("name","") for e in map1["events"] if e]}')

# Weapons確認
wjson = json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Weapons.json', encoding='utf-8'))
print(f"\n=== オノマトペ武器 ===")
for w in wjson:
    if w and w.get('id') in [1,2,51,52]:
        print(f'ID={w["id"]} name={w["name"]}')
