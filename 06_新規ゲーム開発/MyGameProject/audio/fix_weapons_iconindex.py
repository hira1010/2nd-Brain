import json

# Weapons.jsonのパス
path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Weapons.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# wtypeIdに応じたデフォルトiconIndexのマッピング
icon_map = {
    0: 97,   # なし
    1: 96,   # Dagger
    2: 97,   # Sword
    3: 98,   # Flail
    4: 99,   # Axe
    5: 100,  # Whip
    6: 101,  # Staff
    7: 102,  # Bow
    8: 103,  # Crossbow
    9: 104,  # Gun
    10: 105, # Claw
    11: 106, # Glove
    12: 107, # Spear
}

fix_count = 0
for weapon in data:
    if weapon is None:
        continue
    if 'iconIndex' not in weapon:
        wtype = weapon.get('wtypeId', 0)
        weapon['iconIndex'] = icon_map.get(wtype, 97)
        print(f'修正: ID={weapon["id"]} name={weapon["name"]} iconIndex={weapon["iconIndex"]}')
        fix_count += 1

# 修正したデータを書き戻す（RPGToolkitの形式に合わせてseparatorsを設定）
with open(path, 'w', encoding='utf-8', newline='') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print(f'\n合計 {fix_count} 件の武器にiconIndexを追加しました')
print('修正完了！')
