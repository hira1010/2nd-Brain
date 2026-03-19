import json
import os

data_dir = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data'

# 全データファイルのiconIndex欠落チェック（Skills, Items, Armors, Weapons）
check_files = {
    'Skills.json': True,
    'Items.json': True,
    'Troops.json': False,
    'Enemies.json': False,
    'States.json': True,
    'Animations.json': True,
}

for filename, check_icon in check_files.items():
    path = os.path.join(data_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    issues = []
    for item in data:
        if item is None:
            continue
        
        if check_icon and 'iconIndex' not in item:
            issues.append(f"  NG: ID={item.get('id')} name={item.get('name', '?')} - iconIndex欠落")
        
        # params配列チェック
        if 'params' in item:
            p = item['params']
            if p is None:
                issues.append(f"  NG: ID={item.get('id')} - paramsがNone")
            elif not isinstance(p, list):
                issues.append(f"  NG: ID={item.get('id')} - paramsが配列でない")
            elif len(p) != 8 and filename in ['Skills.json', 'Items.json', 'States.json']:
                issues.append(f"  NG: ID={item.get('id')} name={item.get('name','?')} - paramsの長さが{len(p)}（8であるべき）")
    
    if issues:
        print(f"[{filename}] 問題あり:")
        for iss in issues:
            print(iss)
    else:
        print(f"[{filename}] 問題なし")

print("\n--- Animations.json の詳細チェック ---")
path = os.path.join(data_dir, 'Animations.json')
with open(path, 'r', encoding='utf-8') as f:
    anims = json.load(f)

print(f"Animations.json: 全{len(anims)}エントリ")
for anim in anims:
    if anim is None:
        continue
    if 'id' not in anim or 'name' not in anim:
        print(f"  NG: 不完全なエントリ: {anim}")
print("Animations チェック完了")
