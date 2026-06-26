import json
import os

filepath = r'c:\Users\hirak\Desktop\2nd-Brain\22_HeroineAdv\game\data\CommonEvents.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ID 22: Click Processing
click_event = {
    "id": 22,
    "name": "[クリック] 部位判定＆処理",
    "trigger": 0,
    "switchId": 1,
    "list": [
        { "code": 122, "indent": 0, "parameters": [16, 16, 1, 0, 1] },
        { "code": 122, "indent": 0, "parameters": [9, 9, 1, 1, 13] },
        { "code": 111, "indent": 0, "parameters": [1, 12, 0, 0, 1] },
        { "code": 122, "indent": 1, "parameters": [12, 12, 2, 0, 1] },
        { "code": 412, "indent": 0, "parameters": [] },
        { "code": 117, "indent": 0, "parameters": [23] },
        { "code": 117, "indent": 0, "parameters": [25] },
        { "code": 117, "indent": 0, "parameters": [24] },
        { "code": 117, "indent": 0, "parameters": [28] },
        { "code": 0, "indent": 0, "parameters": [] }
    ]
}

# ID 24: UI update (Refinement)
ui_event = {
    "id": 24,
    "name": "[UI] 情報表示更新",
    "trigger": 0,
    "switchId": 1,
    "list": [
        { "code": 355, "indent": 0, "parameters": ["PluginManager.callCommand(this, 'TextPicture', 'set', { text: '\\\\C[0]親密度: \\\\V[9]  所持金: \\\\G' });"] },
        { "code": 231, "indent": 0, "parameters": [10, "", 0, 0, 20, 40, 100, 100, 255, 0] },
        { "code": 355, "indent": 0, "parameters": ["PluginManager.callCommand(this, 'TextPicture', 'set', { text: '\\\\C[14]機嫌値: \\\\V[12] / 100' });"] },
        { "code": 231, "indent": 0, "parameters": [11, "", 0, 0, 20, 80, 100, 100, 255, 0] },
        { "code": 0, "indent": 0, "parameters": [] }
    ]
}

# ID 26: Sell Cheki
sell_event = {
    "id": 26,
    "name": "[経済] チェキ売却",
    "trigger": 0,
    "switchId": 1,
    "list": [
        { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""] },
        { "code": 401, "indent": 0, "parameters": ["撮影したチェキを売却して資金を得よう。"] },
        { "code": 111, "indent": 0, "parameters": [1, 6, 0] },
        { "code": 122, "indent": 1, "parameters": [11, 11, 0, 0, 500] },
        { "code": 126, "indent": 1, "parameters": [6, 1, 0, 1] },
        { "code": 411, "indent": 0, "parameters": [] },
        { "code": 111, "indent": 1, "parameters": [1, 7, 0] },
        { "code": 122, "indent": 2, "parameters": [11, 11, 0, 0, 2000] },
        { "code": 126, "indent": 2, "parameters": [7, 1, 0, 1] },
        { "code": 411, "indent": 1, "parameters": [] },
        { "code": 111, "indent": 2, "parameters": [1, 8, 0] },
        { "code": 122, "indent": 3, "parameters": [11, 11, 0, 0, 10000] },
        { "code": 126, "indent": 3, "parameters": [8, 1, 0, 1] },
        { "code": 411, "indent": 2, "parameters": [] },
        { "code": 101, "indent": 3, "parameters": ["", 0, 0, 2, ""] },
        { "code": 401, "indent": 3, "parameters": ["売却できるチェキを持っていない。"] },
        { "code": 115, "indent": 3, "parameters": [] },
        { "code": 412, "indent": 2, "parameters": [] },
        { "code": 412, "indent": 1, "parameters": [] },
        { "code": 412, "indent": 0, "parameters": [] },
        { "code": 125, "indent": 0, "parameters": [0, 1, 1, 11] },
        { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""] },
        { "code": 401, "indent": 0, "parameters": ["チェキが高く売れた！"] },
        { "code": 401, "indent": 0, "parameters": ["\\\\V[11] G を手に入れた。"] },
        { "code": 250, "indent": 0, "parameters": [{ "name": "Coin", "pan": 0, "pitch": 100, "volume": 90 }] },
        { "code": 117, "indent": 0, "parameters": [24] },
        { "code": 0, "indent": 0, "parameters": [] }
    ]
}

# ID 27: Take Cheki
take_event = {
    "id": 27,
    "name": "[経済] チェキ撮影",
    "trigger": 0,
    "switchId": 1,
    "list": [
        { "code": 250, "indent": 0, "parameters": [{ "name": "Camera", "pan": 0, "pitch": 100, "volume": 90 }] },
        { "code": 111, "indent": 0, "parameters": [1, 10, 0, 0, 1] },
        { "code": 126, "indent": 1, "parameters": [6, 0, 0, 1] },
        { "code": 411, "indent": 0, "parameters": [] },
        { "code": 111, "indent": 1, "parameters": [1, 10, 0, 0, 2] },
        { "code": 126, "indent": 2, "parameters": [7, 0, 0, 1] },
        { "code": 411, "indent": 1, "parameters": [] },
        { "code": 126, "indent": 2, "parameters": [8, 0, 0, 1] },
        { "code": 412, "indent": 1, "parameters": [] },
        { "code": 412, "indent": 0, "parameters": [] },
        { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""] },
        { "code": 401, "indent": 0, "parameters": ["チェキを撮影した！"] },
        { "code": 0, "indent": 0, "parameters": [] }
    ]
}

# ID 28: Rank Up
rank_event = {
    "id": 28,
    "name": "[進行] ランクアップ判定",
    "trigger": 0,
    "switchId": 1,
    "list": [
        { "code": 111, "indent": 0, "parameters": [1, 10, 0, 0, 1] },
        { "code": 111, "indent": 1, "parameters": [1, 9, 0, 2, 100] },
        { "code": 122, "indent": 2, "parameters": [10, 10, 0, 0, 2] },
        { "code": 101, "indent": 2, "parameters": ["", 0, 0, 2, ""] },
        { "code": 401, "indent": 2, "parameters": ["響子との親密度が深まり、ランクが2に上がった！"] },
        { "code": 231, "indent": 2, "parameters": [2, "kyoko_2_blush", 1, 0, 408, 312, 100, 100, 255, 0] },
        { "code": 412, "indent": 1, "parameters": [] },
        { "code": 411, "indent": 0, "parameters": [] },
        { "code": 111, "indent": 1, "parameters": [1, 10, 0, 0, 2] },
        { "code": 111, "indent": 2, "parameters": [1, 9, 0, 2, 500] },
        { "code": 122, "indent": 3, "parameters": [10, 10, 0, 0, 3] },
        { "code": 101, "indent": 3, "parameters": ["", 0, 0, 2, ""] },
        { "code": 401, "indent": 3, "parameters": ["響子との親密度が最大に達し、ランクが3に上がった！"] },
        { "code": 231, "indent": 3, "parameters": [2, "kyoko_3_disheveled", 1, 0, 408, 312, 100, 100, 255, 0] },
        { "code": 412, "indent": 2, "parameters": [] },
        { "code": 412, "indent": 1, "parameters": [] },
        { "code": 412, "indent": 0, "parameters": [] },
        { "code": 0, "indent": 0, "parameters": [] }
    ]
}

# Update function
def update_event(event_obj):
    eid = event_obj['id']
    while len(data) <= eid:
        data.append(None)
    data[eid] = event_obj

update_event(click_event)
update_event(ui_event)
update_event(sell_event)
update_event(take_event)
update_event(rank_event)

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("CommonEvents.json updated successfully.")
