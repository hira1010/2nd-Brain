const fs = require('fs');
const path = require('path');

const PROJECTS = [
    "C:/Users/hirak/Documents/RMMZ/Project1",
    "C:/Users/hirak/Documents/Games/Project1"
];

const hEvent = (id, x, y) => ({
    "id": id, "name": "Hイベント", "note": "",
    "pages": [{
        "conditions": { "actorId": 1, "actorValid": false, "itemId": 1, "itemValid": false, "selfSwitchCh": "A", "selfSwitchValid": false, "switch1Id": 1, "switch1Valid": false, "switch2Id": 1, "switch2Valid": false, "variableId": 1, "variableValid": false, "variableValue": 0 },
        "directionFix": false,
        "image": { "tileId": 0, "characterName": "SF_Actor3", "direction": 2, "pattern": 1, "characterIndex": 3 },
        "list": [
            { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
            { "code": 401, "indent": 0, "parameters": ["あ、あなた……。"] },
            { "code": 231, "indent": 0, "parameters": [1, "heroine_01", 0, 0, 0, 0, 100, 100, 255, 0] },
            { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
            { "code": 401, "indent": 0, "parameters": ["んぁっ……、そんな……奥まで……っ！？"] },
            { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__116おくきたぁ", "pan": 0, "pitch": 100, "volume": 100 }] },
            { "code": 221, "indent": 0, "parameters": [5, 5, 20, true] },
            { "code": 222, "indent": 0, "parameters": [[255, 255, 255, 255], 3, 20, true] },
            { "code": 235, "indent": 0, "parameters": [1] },
            { "code": 0, "indent": 0, "parameters": [] }
        ],
        "moveFrequency": 3, "moveRoute": { "list": [{ "code": 0, "parameters": [] }], "repeat": true, "skippable": false, "wait": false },
        "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": true, "through": false, "trigger": 0, "walkAnime": true
    }],
    "x": x, "y": y
});

const caveEvent = (id, x, y) => ({
    "id": id, "name": "洞窟乳首", "note": "",
    "pages": [{
        "conditions": { "actorId": 1, "actorValid": false, "itemId": 1, "itemValid": false, "selfSwitchCh": "A", "selfSwitchValid": false, "switch1Id": 1, "switch1Valid": false, "switch2Id": 1, "switch2Valid": false, "variableId": 1, "variableValid": false, "variableValue": 0 },
        "directionFix": false,
        "image": { "tileId": 0, "characterName": "", "direction": 2, "pattern": 0, "characterIndex": 0 },
        "list": [
            { "code": 231, "indent": 0, "parameters": [2, "heroine_02", 0, 0, 0, 0, 100, 100, 255, 0] },
            { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__93いっぱい出してぇ！！", "pan": 0, "pitch": 100, "volume": 100 }] },
            { "code": 222, "indent": 0, "parameters": [[255, 255, 255, 255], 5, 10, true] },
            { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "ヒロイン"] },
            { "code": 401, "indent": 0, "parameters": ["んぁっ！ 乳首から溢れちゃうぅぅ！！"] },
            { "code": 235, "indent": 0, "parameters": [2] },
            { "code": 0, "indent": 0, "parameters": [] }
        ],
        "moveFrequency": 3, "moveRoute": { "list": [{ "code": 0, "parameters": [] }], "repeat": true, "skippable": false, "wait": false },
        "moveSpeed": 3, "moveType": 0, "priorityType": 0, "stepAnime": false, "through": false, "trigger": 1, "walkAnime": true
    },
    {
        "conditions": { "actorId": 1, "actorValid": false, "itemId": 1, "itemValid": false, "selfSwitchCh": "A", "selfSwitchValid": false, "switch1Id": 1, "switch1Valid": false, "switch2Id": 1, "switch2Valid": false, "variableId": 1, "variableValid": false, "variableValue": 0 },
        "directionFix": false,
        "image": { "tileId": 0, "characterName": "", "direction": 2, "pattern": 0, "characterIndex": 0 },
        "list": [
            { "code": 231, "indent": 0, "parameters": [2, "heroine_02", 0, 0, 0, 0, 100, 100, 255, 0] },
            { "code": 250, "indent": 0, "parameters": [{ "name": "AnyConv.com__93いっぱい出してぇ！！", "pan": 0, "pitch": 100, "volume": 100 }] },
            { "code": 222, "indent": 0, "parameters": [[255, 255, 255, 255], 5, 10, true] },
            { "code": 235, "indent": 0, "parameters": [2] },
            { "code": 0, "indent": 0, "parameters": [] }
        ],
        "moveFrequency": 3, "moveRoute": { "list": [{ "code": 0, "parameters": [] }], "repeat": true, "skippable": false, "wait": false },
        "moveSpeed": 3, "moveType": 0, "priorityType": 0, "stepAnime": false, "through": false, "trigger": 0, "walkAnime": true
    }],
    "x": x, "y": y
});

PROJECTS.forEach(proj => {
    const mapFile = path.join(proj, "data/Map001.json");
    if (!fs.existsSync(mapFile)) return;
    const map = JSON.parse(fs.readFileSync(mapFile, 'utf8'));
    
    // Reset events to clean state or specific IDs
    if (!map.events) map.events = [null];
    
    // Add multiple events at likely coordinates just in case
    map.events[3] = hEvent(3, 9, 6);  // Harold's right
    map.events[4] = caveEvent(4, 8, 5); // Hole center
    map.events[5] = caveEvent(5, 7, 5); // Left hole
    map.events[6] = caveEvent(6, 9, 5); // Right hole
    map.events[7] = hEvent(7, 7, 6);  // Harold's left
    
    fs.writeFileSync(mapFile, JSON.stringify(map, null, 0));
    console.log(`Updated ${mapFile}`);
});
