import json

# System.jsonを修正してwindowOpacityを追加
path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\System.json'

# バックアップ作成
import shutil
shutil.copy(path, path + '.bak')

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# advancedオブジェクトにwindowOpacityを追加（デフォルト値: 192）
if 'advanced' in data:
    if 'windowOpacity' not in data['advanced']:
        data['advanced']['windowOpacity'] = 192
        print(f"windowOpacity=192 を追加しました")
    else:
        print(f"windowOpacity は既に存在します: {data['advanced']['windowOpacity']}")
else:
    print("ERROR: advancedフィールドがありません")
    exit(1)

# 保存
with open(path, 'w', encoding='utf-8', newline='') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print("System.json を修正しました！")
print(f"advanced: {json.dumps(data['advanced'], ensure_ascii=False)}")
