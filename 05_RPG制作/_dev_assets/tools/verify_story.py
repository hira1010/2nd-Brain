import json

# ============================================================
# 追加されたNPC/イベントの確認
# ============================================================

def check_map(path, label):
    data = json.load(open(path, encoding='utf-8'))
    events = [e for e in data['events'] if e]
    print(f"=== {label} ===")
    print(f"  総イベント数: {len(events)}")
    for e in events:
        name = e['name']
        pages = e.get('pages', [])
        # セリフの最初の行を取得
        first_line = ""
        for page in pages[:1]:
            for cmd in page.get('list', []):
                if cmd['code'] == 401:
                    first_line = cmd['parameters'][0][:20]
                    break
        print(f"  ID={e['id']:3d} ({e['x']:2d},{e['y']:2d}) {name} | {first_line}...")
    print()

check_map(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json', 'Map001')
check_map(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json', 'Map002')

# JSONとして正しく読み込めるか最終チェック
try:
    json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json', encoding='utf-8'))
    json.load(open(r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json', encoding='utf-8'))
    print("✅ JSON整合性チェック: 両マップとも問題なし！")
except Exception as e:
    print(f"❌ JSONエラー: {e}")
