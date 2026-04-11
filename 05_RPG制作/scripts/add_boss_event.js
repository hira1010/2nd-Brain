const fs = require('fs');
const path = require('path');

function addBossEvent(projectPath) {
    const mapFile = path.join(projectPath, 'data', 'Map001.json');
    let data;
    try {
        data = JSON.parse(fs.readFileSync(mapFile, 'utf8'));
    } catch (e) {
        console.error('Failed to read Map001.json', e);
        return;
    }

    // Boss Event (ID 6) at (10, 15)
    // Image: Monster (ID 4 in Enemies.json)
    const bossEvent = {
        "id": 6,
        "name": "オノマトペ大魔王",
        "note": "<ABS>\n<Type: Enemy>\n<ID: 4>",
        "pages": [
            {
                "conditions": {
                    "actorId": 1, "actorValid": false,
                    "itemId": 1, "itemValid": false,
                    "selfSwitchCh": "A", "selfSwitchValid": false,
                    "switch1Id": 1, "switch1Valid": false,
                    "switch2Id": 1, "switch2Valid": false,
                    "variableId": 1, "variableValid": false,
                    "variableValue": 0
                },
                "directionFix": false,
                "image": {
                    "characterIndex": 3,
                    "characterName": "Monster",
                    "direction": 2,
                    "pattern": 1,
                    "tileId": 0
                },
                "list": [
                    { "code": 0, "indent": 0, "parameters": [] }
                ],
                "moveFrequency": 3,
                "moveRoute": {
                    "list": [{ "code": 0, "parameters": [] }],
                    "repeat": true, "skippable": false, "wait": false
                },
                "moveSpeed": 3,
                "moveType": 0,
                "priorityType": 1,
                "stepAnime": true,
                "through": false,
                "trigger": 0,
                "walkAnime": true
            }
        ],
        "x": 10,
        "y": 15
    };

    // Ensure events array can accommodate ID 6
    if (!data.events) data.events = [];
    while (data.events.length <= 6) {
        data.events.push(null);
    }
    data.events[6] = bossEvent;

    fs.writeFileSync(mapFile, JSON.stringify(data, null, 2));
    console.log('Successfully added Boss Event to Map001');
}

addBossEvent('c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作');
