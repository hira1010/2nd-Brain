const fs = require('fs');
const path = require('path');

function addStageClearEvent(projectPath) {
    const ceFile = path.join(projectPath, 'data', 'CommonEvents.json');
    let data;
    try {
        data = JSON.parse(fs.readFileSync(ceFile, 'utf8'));
    } catch (e) {
        console.error('Failed to read CommonEvents.json', e);
        return;
    }

    const clearEvent = {
        "id": 10,
        "name": "ステージクリア演出",
        "switchId": 1,
        "trigger": 0,
        "list": [
            { "code": 231, "indent": 0, "parameters": [1, "StageClear", 1, 0, 408, 312, 100, 100, 255, 0] }, // Show Picture
            { "code": 230, "indent": 0, "parameters": [180] }, // Wait 3 seconds
            { "code": 354, "indent": 0, "parameters": [] }, // Return to Title Screen
            { "code": 0, "indent": 0, "parameters": [] }
        ]
    };

    // Ensure common events array can accommodate ID 10
    while (data.length <= 10) {
        data.push(null);
    }
    data[10] = clearEvent;

    fs.writeFileSync(ceFile, JSON.stringify(data, null, 2));
    console.log('Successfully added Stage Clear Common Event');
}

addStageClearEvent('c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作');
