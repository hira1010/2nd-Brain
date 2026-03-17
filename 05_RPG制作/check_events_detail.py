import json

# Map001の全イベント詳細確認
m1 = json.load(open('data/Map001.json', encoding='utf-8'))
print('=== Map001 イベント詳細 ===')
for e in m1['events']:
    if e:
        print(f'\n[ID={e["id"]} name={e["name"]} x={e["x"]} y={e["y"]}]')
        for i, page in enumerate(e.get('pages', [])):
            cmds = page.get('list', [])
            texts = [c for c in cmds if c['code'] in [101, 401, 102]]
            if texts:
                print(f'  page{i}: ', end='')
                for t in texts[:3]:
                    if t['code'] == 401:
                        print(f'"{t["parameters"][0]}"', end=' ')
                    elif t['code'] == 101:
                        print(f'[顔/名前]', end=' ')
                print()

print()
print('=== Map002 イベント詳細 ===')
m2 = json.load(open('data/Map002.json', encoding='utf-8'))
for e in m2['events']:
    if e:
        print(f'\n[ID={e["id"]} name={e["name"]} x={e["x"]} y={e["y"]}]')
        for i, page in enumerate(e.get('pages', [])):
            cmds = page.get('list', [])
            texts = [c for c in cmds if c['code'] in [101, 401, 102]]
            if texts:
                print(f'  page{i}: ', end='')
                for t in texts[:3]:
                    if t['code'] == 401:
                        print(f'"{t["parameters"][0]}"', end=' ')
                    elif t['code'] == 101:
                        print(f'[顔/名前]', end=' ')
                print()
