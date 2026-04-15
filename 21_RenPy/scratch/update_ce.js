const fs = require('fs');
const path = require('path');

const filepath = 'c:\\Users\\hirak\\Desktop\\2nd-Brain\\22_HeroineAdv\\game\\data\\CommonEvents.json';
const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));

// ID 22: Click Processing
const click_event = {
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
};

// ID 24: UI Update
const ui_event = {
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
};

// ID 27: Take Cheki
const take_event = {
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
};

// ID 28: Rank Up
const rank_event = {
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
};

const updateEvent = (event) => {
    while (data.length <= event.id) data.push(null);
    data[event.id] = event;
};

updateEvent(click_event);
updateEvent(ui_event);
updateEvent(take_event);
updateEvent(rank_event);

fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf8');
console.log('CommonEvents.json updated.');
