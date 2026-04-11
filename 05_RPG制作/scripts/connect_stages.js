const fs = require('fs');
const path = require('path');

const DATA_DIR = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\05_RPG制作\\data";

// [CurrentMap, NextMap]
const CONNECTION_PLAN = [
    { from: 1, to: 2, fx: 19, fy: 10, tx: 1, ty: 6 },  // 1 -> 2
    { from: 2, to: 8, fx: 16, fy: 6, tx: 1, ty: 10 }, // 2 -> 8
    { from: 8, to: 5, fx: 10, fy: 19, tx: 10, ty: 1 }, // 8 -> 5
    { from: 5, to: 4, fx: 19, fy: 10, tx: 1, ty: 10 }, // 5 -> 4
    { from: 4, to: 7, fx: 10, fy: 19, tx: 10, ty: 1 }, // 4 -> 7
    { from: 7, to: 6, fx: 10, fy: 19, tx: 10, ty: 1 }  // 7 -> 6
];

function ensureFloor(mapData, mapId) {
    const width = mapData.width;
    const height = mapData.height;
    const layer0 = mapData.data.slice(0, width * height);
    
    // Check if Layer 0 is all 0
    const isEmpty = layer0.every(t => t === 0);
    if (isEmpty) {
        console.log(`Map ${mapId} is empty. Filling floor...`);
        let floorTile = 2816; // Grass
        if ([4, 5, 8, 6].includes(mapId)) floorTile = 3200; // Dungeon/Stone
        
        for (let i = 0; i < width * height; i++) {
            mapData.data[i] = floorTile;
        }
    }
}

function addWarp(fromId, toId, fx, fy, tx, ty) {
    const filename = `Map${fromId.toString().padStart(3, '0')}.json`;
    const filepath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filepath)) return;

    const mapData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    ensureFloor(mapData, fromId);

    // Add Warp Event
    const warpEvent = {
        id: mapData.events.length,
        name: "StageExit",
        note: "",
        pages: [{
            conditions: { actorId: 1, actorValid: false, itemId: 1, itemValid: false, selfSwitchCh: "A", selfSwitchValid: false, switch1Id: 1, switch1Valid: false, switch2Id: 1, switch2Valid: false, variableId: 1, variableValid: false, variableValue: 0 },
            directionFix: false,
            image: { characterIndex: 0, characterName: "!Crystal", direction: 2, pattern: 0, tileId: 0 },
            list: [
                { code: 250, indent: 0, parameters: [{ name: "Move1", pan: 0, pitch: 100, volume: 90 }] }, // SE
                { code: 201, indent: 0, parameters: [0, toId, tx, ty, 0, 0] }, // Transfer
                { code: 0, indent: 0, parameters: [] }
            ],
            moveFrequency: 3,
            moveRoute: { list: [{ code: 0, parameters: [] }], repeat: true, skiable: false, wait: false },
            moveSpeed: 3,
            moveType: 0,
            priorityType: 1,
            stepAnime: true,
            through: false,
            trigger: 0, // Action Button
            walkAnime: true
        }],
        x: fx,
        y: fy
    };

    if (!Array.isArray(mapData.events)) mapData.events = [null];
    mapData.events.push(warpEvent);

    fs.writeFileSync(filepath, JSON.stringify(mapData, null, 2), 'utf8');
}

CONNECTION_PLAN.forEach(p => {
    addWarp(p.from, p.to, p.fx, p.fy, p.tx, p.ty);
    // Also ensure floor for the destination of the last one
    if (p.to === 6) {
        const destPath = path.join(DATA_DIR, `Map006.json`);
        if (fs.existsSync(destPath)) {
            const destData = JSON.parse(fs.readFileSync(destPath, 'utf8'));
            ensureFloor(destData, 6);
            fs.writeFileSync(destPath, JSON.stringify(destData, null, 2), 'utf8');
        }
    }
});

console.log("Map connections and floor filling complete!");
