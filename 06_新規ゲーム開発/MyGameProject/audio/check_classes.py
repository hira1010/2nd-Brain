import json

# Classes.jsonの詳細解析
path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Classes.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Classes.json: 全{len(data)}エントリ")
print()

for cls in data:
    if cls is None:
        continue
    
    class_id = cls.get('id')
    name = cls.get('name', '?')
    params = cls.get('params', None)
    
    if params is None:
        print(f"[ID:{class_id}] {name}: params=None (欠落!)")
    elif not isinstance(params, list):
        print(f"[ID:{class_id}] {name}: paramsが配列でない type={type(params)}")
    else:
        print(f"[ID:{class_id}] {name}: params.len={len(params)}")
        for i, row in enumerate(params):
            if not isinstance(row, list):
                print(f"  → params[{i}]が配列でない: {row}")
            else:
                print(f"  → params[{i}].len={len(row)} [0]={row[0] if row else 'empty'}")
