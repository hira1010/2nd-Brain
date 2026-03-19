const fs = require('fs');
const path = require('path');

const PROJECTS = [
    "C:/Users/hirak/Documents/RMMZ/Project1",
    "C:/Users/hirak/Documents/Games/Project1"
];

const hEvent = (id, x, y) => ({
    "id": id, "name": "H-NPC", "note": "",
    "pages": [{
        "conditions": { "actorId": 1, "actorValid": false, "itemId": 1, "itemValid": false, "selfSwitchCh": "A", "selfSwitchValid": false, "switch1Id": 1, "switch1Valid": false, "switch2Id": 1, "switch2Valid": false, "variableId": 1, "variableValid": false, "variableValue": 0 },
        "directionFix": false,
        "image": { "tileId": 0, "characterName": "SF_Actor3", "direction": 2, "pattern": 1, "characterIndex": 3 },
        "list": [
            { "code": 101, "indent": 0, "parameters": ["", 0, 0, 2, "リア"] },
            { "code": 401, "indent": 0, "parameters": ["あ、あなた……。"] },
            { "code": 231, "indent": 0, "parameters": [1, "heroine_01", 0, 0, 0, 0, 100, 100, 255, 0] },
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

const sprayEvent = (id, x, y) => ({
    "id": id, "name": "噴射演出", "note": "",
    "pages": [{
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
    const dataDir = path.join(proj, "data");
    if (!fs.existsSync(dataDir)) return;
    
    fs.readdirSync(dataDir).filter(f => f.startsWith('Map') && f.endsWith('.json')).forEach(f => {
        const mapPath = path.join(dataDir, f);
        const map = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
        const width = map.width;
        const height = map.height;
        
        // Find ALL hole-like tiles
        const targetCoords = [];
        const targetTiles = [52, 3, 3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3376, 3377, 3378, 3379, 3380, 3381, 3382, 3383];
        
        for (let l = 0; l < 6; l++) {
            for (let i = 0; i < width * height; i++) {
                if (targetTiles.includes(map.data[l * width * height + i])) {
                    targetCoords.push({ x: i % width, y: Math.floor(i / width) });
                }
            }
        }
        
        if (targetCoords.length > 0 || f === 'Map001.json') {
            console.log(`Updating ${mapPath}...`);
            if (!map.events) map.events = [null];
            
            // Add spray events to all hole coords
            targetCoords.forEach((c, idx) => {
                map.events[idx + 10] = sprayEvent(idx + 10, c.x, c.y);
            });
            
            // Add NPCs to Harold's vicinity in Map001
            if (f === 'Map001.json') {
                map.events[3] = hEvent(3, 9, 6);
                map.events[4] = hEvent(4, 7, 6);
                map.events[5] = hEvent(5, 8, 7);
                map.events[6] = hEvent(6, 11, 10); // ID 3 cluster
                map.events[7] = hEvent(7, 10, 10);
            }
            
            fs.writeFileSync(mapPath, JSON.stringify(map, null, 0));
        }
    });
});
