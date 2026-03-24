import json

path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Weapons.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

found_issues = False
for w in data:
    if w is None:
        continue
    if 'iconIndex' not in w:
        print(f'NG: ID={w["id"]} name={w["name"]} - iconIndex欠落')
        found_issues = True
    elif w['id'] in [1, 2, 51, 52]:
        print(f'OK: ID={w["id"]} name={w["name"]} iconIndex={w["iconIndex"]}')

if not found_issues:
    print('全武器のiconIndex問題なし！')
print('検証完了')
