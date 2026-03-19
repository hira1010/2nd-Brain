import json, shutil

# Map002.jsonを修正: 洞窟タイルセット(ID=4 Dungeon)に変更 + エンカウント設定追加
path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json'
shutil.copy(path, path + '.bak')

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# タイルセットをDungeon(ID=4)に変更
data['tilesetId'] = 4

# エンカウントリストを設定（Troop ID=1,2,3などを使用）
# encounterStep=30はデフォルト歩数でランダムエンカウント
data['encounterList'] = [
    {"regionSet": [], "troopId": 1, "weight": 10},   # Goblin*2
    {"regionSet": [], "troopId": 2, "weight": 10},   # 別のトループ
    {"regionSet": [], "troopId": 3, "weight": 5},    # 強いトループ
]
data['encounterStep'] = 20  # 20歩ごとにエンカウント発生（少ない=多くエンカウント）

# マップ名を設定
data['displayName'] = '洞窟'

# バトルバックを洞窟風に設定
data['specifyBattleback'] = True
data['battleback1Name'] = 'Cave'
data['battleback2Name'] = 'Cave'

with open(path, 'w', encoding='utf-8', newline='') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print("Map002.json 修正完了！")
print(f"tilesetId: {data['tilesetId']} (4=Dungeon)")
print(f"encounterList: {len(data['encounterList'])}件のトループ設定")
print(f"encounterStep: {data['encounterStep']}")
print(f"displayName: {data['displayName']}")
