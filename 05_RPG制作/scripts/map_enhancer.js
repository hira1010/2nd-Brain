const fs = require('fs');
const path = require('path');

const DATA_DIR = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\05_RPG制作\\data";

const STAGES = {
    1: { name: "1. 欲望の平原", bgm: "Field1", tint: [0, 0, 0, 0] },
    2: { name: "2. 蜜の滴る大森林", bgm: "Ship3", tint: [-34, 0, -34, 34] },
    8: { name: "3. 情熱の灼熱火山", bgm: "Dungeon1", tint: [60, -30, -60, 60] },
    5: { name: "4. 凍える吐息の氷穴", bgm: "Dungeon2", tint: [-60, -30, 60, 60] },
    4: { name: "5. 背徳の地下迷宮", bgm: "Dungeon3", tint: [-100, -100, -100, 150] },
    7: { name: "6. 桃源郷の空中庭園", bgm: "Field2", tint: [30, 30, 60, 0] },
    6: { name: "7. 淫欲の魔王宮", bgm: "Theme4", tint: [40, -40, -40, 80] }
};

function enhanceMap(mapId, config) {
    const filename = `Map${mapId.toString().padStart(3, '0')}.json`;
    const filepath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filepath)) {
        console.log(`Skipping ${filename}: File not found.`);
        return;
    }

    console.log(`Enhancing ${filename} (${config.name})...`);
    
    // Backup
    fs.copyFileSync(filepath, filepath + ".bak_js_enhancer");

    const mapData = JSON.parse(fs.readFileSync(filepath, 'utf8'));

    // 1. Basic Settings
    mapData.displayName = config.name;
    mapData.bgm.name = config.bgm;
    mapData.autoplayBgm = true;

    // 2. Tile Decoration (Layer 3)
    const width = mapData.width;
    const height = mapData.height;
    const layerSize = width * height;
    const decorTiles = [1, 2, 8, 5, 7].includes(mapId) 
        ? [16, 17, 18, 32, 33, 34] 
        : [192, 193, 200, 201];

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const idx = 3 * layerSize + (y * width + x);
            if (mapData.data[idx] === 0 && Math.random() < 0.12) {
                mapData.data[idx] = decorTiles[Math.floor(Math.random() * decorTiles.length)];
            }
        }
    }

    // 3. Environment Tint Event
    if (!Array.isArray(mapData.events)) {
        mapData.events = [null];
    }
    
    const tintEvent = {
        id: mapData.events.length, // Array length becomes the next ID (roughly)
        name: "Env_Tint",
        note: "",
        pages: [{
            conditions: { actorId: 1, actorValid: false, itemId: 1, itemValid: false, selfSwitchCh: "A", selfSwitchValid: false, switch1Id: 1, switch1Valid: false, switch2Id: 1, switch2Valid: false, variableId: 1, variableValid: false, variableValue: 0 },
            directionFix: false,
            image: { characterIndex: 0, characterName: "", direction: 2, pattern: 0, tileId: 0 },
            list: [
                { code: 223, indent: 0, parameters: [config.tint, 60, true] },
                { code: 214, indent: 0, parameters: [] },
                { code: 0, indent: 0, parameters: [] }
            ],
            moveFrequency: 3,
            moveRoute: { list: [{ code: 0, parameters: [] }], repeat: true, skippable: false, wait: false },
            moveSpeed: 3,
            moveType: 0,
            priorityType: 0,
            stepAnime: false,
            through: false,
            trigger: 3,
            walkAnime: true
        }],
        x: 0,
        y: 0
    };
    mapData.events.push(tintEvent);

    fs.writeFileSync(filepath, JSON.stringify(mapData, null, 2), 'utf8');
}

function updateMapInfos() {
    const infoPath = path.join(DATA_DIR, "MapInfos.json");
    if (!fs.existsSync(infoPath)) return;
    
    fs.copyFileSync(infoPath, infoPath + ".bak_js_enhancer");
    const infos = JSON.parse(fs.readFileSync(infoPath, 'utf8'));

    infos.forEach(info => {
        if (info && STAGES[info.id]) {
            info.name = STAGES[info.id].name;
        }
    });

    fs.writeFileSync(infoPath, JSON.stringify(infos, null, 2), 'utf8');
}

updateMapInfos();
Object.keys(STAGES).forEach(id => enhanceMap(parseInt(id), STAGES[id]));
console.log("Map enhancement complete via JS!");
