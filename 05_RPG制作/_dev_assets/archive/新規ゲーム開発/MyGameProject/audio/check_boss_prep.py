import json

# Enemies確認
enemies = json.load(open('data/Enemies.json', encoding='utf-8'))
print('=== Enemies ===')
for e in enemies:
    if e:
        params = e.get('params', [])
        print(f'ID={e["id"]} name={e["name"]}')
        print(f'  HP={params[0] if len(params)>0 else "?"} MP={params[1] if len(params)>1 else "?"}')
        print(f'  ATK={params[2] if len(params)>2 else "?"} DEF={params[3] if len(params)>3 else "?"}')
        print(f'  EXP={e.get("exp","?")} GOLD={e.get("gold","?")}')
        drops = e.get('dropItems', [])
        print(f'  drops={[(d.get("kind"),d.get("dataId")) for d in drops if d.get("kind",0)>0]}')
        print()

# Troops確認
troops = json.load(open('data/Troops.json', encoding='utf-8'))
print('=== Troops ===')
for t in troops:
    if t:
        print(f'ID={t["id"]} name={t["name"]}')
        for m in t.get('members', []):
            print(f'  enemyId={m.get("enemyId")} x={m.get("x")} y={m.get("y")}')
        pages = t.get('pages', [])
        print(f'  battleEventPages={len(pages)}')
        print()

# Map002イベント確認（ボス配置場所の空きチェック）
m2 = json.load(open('data/Map002.json', encoding='utf-8'))
print('=== Map002 イベント位置一覧 ===')
for e in m2['events']:
    if e:
        print(f'  ID={e["id"]} ({e["x"]},{e["y"]}) {e["name"]}')
print(f'  マップサイズ: {m2["width"]}x{m2["height"]}')
