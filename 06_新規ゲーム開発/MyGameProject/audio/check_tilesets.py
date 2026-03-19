import json

# Tilesets確認
path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Tilesets.json'
data = json.load(open(path, encoding='utf-8'))
for t in data:
    if t:
        print(f'ID={t["id"]} name={t["name"]} mode={t["mode"]}')
