import json

# 全JSONの整合性チェック
files = {
    'Enemies': r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Enemies.json',
    'Troops':  r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Troops.json',
    'Map002':  r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json',
}

for name, path in files.items():
    try:
        data = json.load(open(path, encoding='utf-8'))
        print(f"OK {name}: {len([x for x in data if x])}件")
    except Exception as e:
        print(f"NG {name}: {e}")

# ボスの内容詳細確認
print()
enemies = json.load(open(files['Enemies'], encoding='utf-8'))
boss = next((e for e in enemies if e and e.get('name') == 'ゴロゴロ大王'), None)
if boss:
    print(f"ボス確認: ID={boss['id']} name={boss['name']}")
    print(f"  HP={boss['params'][0]} ATK={boss['params'][2]} EXP={boss['exp']} GOLD={boss['gold']}")

troops = json.load(open(files['Troops'], encoding='utf-8'))
boss_troop = next((t for t in troops if t and 'ゴロゴロ大王' in t.get('name','')), None)
if boss_troop:
    print(f"ボストループ確認: ID={boss_troop['id']} name={boss_troop['name']}")

m2 = json.load(open(files['Map002'], encoding='utf-8'))
boss_ev = next((e for e in m2['events'] if e and 'ゴロゴロ大王' in e.get('name','')), None)
if boss_ev:
    print(f"ボスイベント確認: ID={boss_ev['id']} 座標=({boss_ev['x']},{boss_ev['y']}) pages={len(boss_ev['pages'])}")

print()
print("全チェック完了！")
