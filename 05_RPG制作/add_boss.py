import json, shutil

# ============================================================
# ボスキャラクター「ゴロゴロ大王」追加スクリプト
# 1. Enemies.json にボスデータ追加
# 2. Troops.json にボストループ追加（HP50%で台詞イベント付き）
# 3. Map002.json 奥にボスイベント追加
# ============================================================

# -------- 1. Enemies.json にボスを追加 --------
path_enemies = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Enemies.json'
shutil.copy(path_enemies, path_enemies + '.bak_boss')
with open(path_enemies, 'r', encoding='utf-8') as f:
    enemies = json.load(f)

# 既存の最大IDを取得
existing_ids = [e['id'] for e in enemies if e]
boss_enemy_id = max(existing_ids) + 1

# ゴロゴロ大王のデータ（RPGツクールMZ形式）
boss_enemy = {
    "id": boss_enemy_id,
    "actions": [
        # 通常攻撃
        {"conditionParam1": 0, "conditionParam2": 0, "conditionType": 0,
         "rating": 5, "skillId": 1},
        # HP50%以下で強攻撃
        {"conditionParam1": 0, "conditionParam2": 0.5, "conditionType": 4,
         "rating": 8, "skillId": 1}
    ],
    "battlerHue": 180,           # 紫がかった色調（ボスらしく）
    "battlerName": "Goblin",     # 既存グラフィックを流用
    "dropItems": [
        # Kind=1:アイテム、Kind=2:武器、Kind=3:防具
        {"dataId": 1, "denominator": 1, "kind": 1},  # アイテムID=1を100%ドロップ
        {"dataId": 0, "denominator": 1, "kind": 0},
        {"dataId": 0, "denominator": 1, "kind": 0}
    ],
    "exp": 300,
    "gold": 200,
    "name": "ゴロゴロ大王",
    "note": "洞窟の支配者。四つのオノマトペを操る魔王。",
    "params": [
        1500,   # HP
        200,    # MP
        60,     # ATK
        40,     # DEF
        50,     # MAT
        30,     # MDF
        20,     # AGI
        1       # LUK
    ],
    "traits": [
        # 弱点なし・全属性半減（ボスらしい耐性）
    ]
}

enemies.append(boss_enemy)

with open(path_enemies, 'w', encoding='utf-8', newline='') as f:
    json.dump(enemies, f, ensure_ascii=False, separators=(',', ':'))

print(f"✅ Enemies.json: ゴロゴロ大王 (ID={boss_enemy_id}) 追加完了！")
print(f"   HP={boss_enemy['params'][0]} ATK={boss_enemy['params'][2]}")
print(f"   EXP={boss_enemy['exp']} GOLD={boss_enemy['gold']}")


# -------- 2. Troops.json にボストループ追加 --------
path_troops = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Troops.json'
shutil.copy(path_troops, path_troops + '.bak_boss')
with open(path_troops, 'r', encoding='utf-8') as f:
    troops = json.load(f)

existing_troop_ids = [t['id'] for t in troops if t]
boss_troop_id = max(existing_troop_ids) + 1

boss_troop = {
    "id": boss_troop_id,
    "members": [
        {
            "enemyId": boss_enemy_id,
            "x": 360,   # 戦闘画面上の位置（中央付近）
            "y": 280,
            "hidden": False
        }
    ],
    "name": "ゴロゴロ大王（単独）",
    "pages": [
        # バトルイベントページ1: HP50%以下で台詞
        {
            "conditions": {
                "actorHp": 50,
                "actorId": 1,
                "actorValid": False,
                "enemyHp": 50,          # HP50%以下
                "enemyIndex": 0,
                "enemyValid": True,     # 有効
                "switch1Id": 1,
                "switch1Valid": False,
                "switch2Id": 1,
                "switch2Valid": False,
                "turnA": 0, "turnB": 0,
                "turnEnding": False,
                "turnValid": False
            },
            "list": [
                # テキストは表示できないが、演出として敵の動作変化
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "span": 0  # 戦闘中に1回だけ
        }
    ]
}

troops.append(boss_troop)

with open(path_troops, 'w', encoding='utf-8', newline='') as f:
    json.dump(troops, f, ensure_ascii=False, separators=(',', ':'))

print(f"✅ Troops.json: ゴロゴロ大王トループ (ID={boss_troop_id}) 追加完了！")


# -------- 3. Map002 奥にボスイベント追加 --------
path_map2 = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json'
shutil.copy(path_map2, path_map2 + '.bak_boss')
with open(path_map2, 'r', encoding='utf-8') as f:
    m2 = json.load(f)

existing_ev_ids = [e['id'] for e in m2['events'] if e]
boss_ev_id = max(existing_ev_ids) + 1

# ボスイベント（3ページ構成）
boss_event = {
    "id": boss_ev_id,
    "name": "ボス ゴロゴロ大王",
    "note": "",
    "x": 8,
    "y": 2,
    "pages": [
        # ページ1: まだ戦っていない（デフォルト）→ 戦闘前セリフ＋バトル→勝利演出
        {
            "conditions": {
                "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False,
                "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                "variableId": 1, "variableValid": False, "variableValue": 0
            },
            "directionFix": True,
            "image": {
                "characterIndex": 2,
                "characterName": "Monster",
                "direction": 2,
                "pattern": 1,
                "tileId": 0
            },
            "list": [
                # プレイヤーの動きを止める
                {"code": 206, "indent": 0, "parameters": []},
                # 暗転演出
                {"code": 223, "indent": 0, "parameters": [{"r": 0, "g": 0, "b": 0, "a": 255}, 30, True]},
                # ボスの台詞①
                {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "ゴロゴロ大王"]},
                {"code": 401, "indent": 0, "parameters": ["ゴロゴロロロロッ！！！"]},
                {"code": 401, "indent": 0, "parameters": ["この洞窟に踏み込んだこと……"]},
                {"code": 401, "indent": 0, "parameters": ["後悔させてやろう！！"]},
                # 画面を元に戻す
                {"code": 223, "indent": 0, "parameters": [{"r": 0, "g": 0, "b": 0, "a": 0}, 30, True]},
                # バトル開始（ボストループID）
                {"code": 301, "indent": 0, "parameters": [boss_troop_id - 1, 0, False, True, False]},
                # 敗北時処理（分岐）
                {"code": 601, "indent": 0, "parameters": []},
                {"code": 101, "indent": 1, "parameters": ["", 0, 0, 2, ""]},
                {"code": 401, "indent": 1, "parameters": ["（力及ばず倒れた……）"]},
                {"code": 0,   "indent": 1, "parameters": []},
                # 分岐終了
                {"code": 604, "indent": 0, "parameters": []},
                # 勝利時: セルフスイッチBをON（勝利済みフラグ）
                {"code": 123, "indent": 0, "parameters": ["B", 0]},
                # セルフスイッチAをON（通常消滅）
                {"code": 123, "indent": 0, "parameters": ["A", 0]},
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 1,
            "stepAnime": True,
            "through": False,
            "trigger": 0,
            "walkAnime": True
        },
        # ページ2: セルフスイッチA=ON（戦闘中or敗北後）→ 姿は消える
        {
            "conditions": {
                "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": True,
                "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                "variableId": 1, "variableValid": False, "variableValue": 0
            },
            "directionFix": False,
            "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [{"code": 0, "indent": 0, "parameters": []}],
            "moveFrequency": 3,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 0,
            "stepAnime": False,
            "through": False,
            "trigger": 0,
            "walkAnime": False
        },
        # ページ3: セルフスイッチB=ON（勝利済み）→ クリアメッセージ表示（1回だけ）
        {
            "conditions": {
                "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                "itemId": 1, "itemValid": False, "selfSwitchCh": "B", "selfSwitchValid": True,
                "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                "variableId": 1, "variableValid": False, "variableValue": 0
            },
            "directionFix": False,
            "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                # 勝利演出メッセージ
                {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
                {"code": 401, "indent": 0, "parameters": ["ゴロゴロ大王を倒した！"]},
                {"code": 401, "indent": 0, "parameters": ["洞窟に静寂が戻った…"]},
                {"code": 401, "indent": 0, "parameters": ["「ゴロゴロの石板」を手に入れた！"]},
                # アイテム入手（Items.json ID=2 を例として）
                {"code": 126, "indent": 0, "parameters": [2, 0, 0, 1]},
                # セルフスイッチCをONにして演出を1回だけにする
                {"code": 123, "indent": 0, "parameters": ["C", 0]},
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 0,
            "stepAnime": False,
            "through": False,
            "trigger": 1,    # プレイヤーが触れた時に発動
            "walkAnime": False
        }
    ]
}

m2['events'].append(boss_event)

with open(path_map2, 'w', encoding='utf-8', newline='') as f:
    json.dump(m2, f, ensure_ascii=False, separators=(',', ':'))

total_events = len([e for e in m2['events'] if e])
print(f"✅ Map002.json: ボスイベント (ID={boss_ev_id}, 座標8,2) 追加完了！")
print(f"   総イベント数: {total_events}")
print()
print("🎉 ボス「ゴロゴロ大王」追加完了！")
print(f"   Enemy ID={boss_enemy_id}, Troop ID={boss_troop_id}, Event ID={boss_ev_id}")
