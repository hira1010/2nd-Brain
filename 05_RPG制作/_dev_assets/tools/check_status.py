import json

# Map001の詳細確認
m1 = json.load(open('data/Map001.json', encoding='utf-8'))
print('=== Map001 ===')
print(f'size: {m1["width"]}x{m1["height"]}')
print(f'displayName: {m1.get("displayName","")}')
print(f'tilesetId: {m1["tilesetId"]}')
print('events:')
for e in m1['events']:
    if e:
        print(f'  ID={e["id"]} name={e["name"]} x={e["x"]} y={e["y"]}')

print()
# Map002の詳細確認
m2 = json.load(open('data/Map002.json', encoding='utf-8'))
print('=== Map002 ===')
print(f'size: {m2["width"]}x{m2["height"]}')
print(f'displayName: {m2.get("displayName","")}')
print(f'tilesetId: {m2["tilesetId"]}')
print('events:')
for e in m2['events']:
    if e:
        print(f'  ID={e["id"]} name={e["name"]} x={e["x"]} y={e["y"]}')

print()
# MapInfos確認
mi = json.load(open('data/MapInfos.json', encoding='utf-8'))
print('=== MapInfos ===')
for m in mi:
    if m:
        print(f'  ID={m["id"]} name={m["name"]}')

print()
# Troops確認
troops = json.load(open('data/Troops.json', encoding='utf-8'))
print('=== Troops ===')
for t in troops:
    if t:
        print(f'  ID={t["id"]} name={t["name"]} members={len(t["members"])}')

print()
# Enemies確認
enemies = json.load(open('data/Enemies.json', encoding='utf-8'))
print('=== Enemies ===')
for e in enemies:
    if e:
        print(f'  ID={e["id"]} name={e["name"]} hp={e["params"][0]}')

print()
# Weapons確認
weapons = json.load(open('data/Weapons.json', encoding='utf-8'))
print('=== Weapons (オノマトペ武器) ===')
for w in weapons:
    if w and w.get('name'):
        print(f'  ID={w["id"]} name={w["name"]} atk_bonus={w["params"][2] if len(w["params"])>2 else "?"}')

print()
# System確認
sys_data = json.load(open('data/System.json', encoding='utf-8'))
print(f'=== System ===')
print(f'startMapId={sys_data.get("startMapId")} x={sys_data.get("startX")} y={sys_data.get("startY")}')
print(f'gameTitle={sys_data.get("gameTitle","未設定")}')
