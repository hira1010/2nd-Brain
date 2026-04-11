const fs = require('fs');
const path = require('path');

const DATA_DIR = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\05_RPG制作\\data";

// ステージごとの複雑度（密度）設定
// 1.0 = 全マス埋まる, 0.0 = 何もなし
const COMPLEXITY_SETTINGS = {
    1: { density: 0.03, cluster: 1, name: "1. 欲望の平原" },
    2: { density: 0.12, cluster: 2, name: "2. 蜜の滴る大森林" },
    8: { density: 0.18, cluster: 3, name: "3. 情熱の灼熱火山" },
    5: { density: 0.25, cluster: 4, name: "4. 凍える吐息の氷穴" },
    4: { density: 0.35, cluster: 6, name: "5. 背徳の地下迷宮" },
    7: { density: 0.28, cluster: 5, name: "6. 桃源郷の空中庭園" },
    6: { density: 0.45, cluster: 8, name: "7. 淫欲の魔王宮" }
};

function refineMap(mapId, config) {
    const filename = `Map${mapId.toString().padStart(3, '0')}.json`;
    const filepath = path.join(DATA_DIR, filename);

    if (!fs.existsSync(filepath)) return;

    console.log(`Refining complexity for Map ${mapId} (${config.name})...`);
    const mapData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
    
    const width = mapData.width;
    const height = mapData.height;
    const layerSize = width * height;

    // Layer 0: 床 (確保済み)
    // Layer 3: 装飾・障害物
    
    // 一旦Layer 3をクリア（前回のランダム装飾をリセット）
    for (let i = 3 * layerSize; i < 4 * layerSize; i++) {
        mapData.data[i] = 0;
    }

    // 障害物タイルの選定
    const obstacleTiles = [4, 5, 8, 6].includes(mapId) 
        ? [3200, 3201] // ダンジョン系なら壁的なもの (タイルAの一部やタイルB)
        : [16, 17, 18, 32, 33, 34]; // 自然系 (Tile B)

    // 複雑度に応じた自動配置
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            // 開始地点 (8,6) と ゴール(水晶) 周辺は空ける
            if (Math.abs(x - 8) < 3 && Math.abs(y - 6) < 3) continue;
            
            const idx = 3 * layerSize + (y * width + x);
            
            // 密度に基づいた配置判定
            if (Math.random() < config.density) {
                // クラスター配置（塊を作る）
                const cWidth = Math.floor(Math.random() * (config.cluster / 2)) + 1;
                const cHeight = Math.floor(Math.random() * (config.cluster / 2)) + 1;
                const tile = obstacleTiles[Math.floor(Math.random() * obstacleTiles.length)];
                
                for (let cy = 0; cy < cHeight; cy++) {
                    for (let cx = 0; cx < cWidth; cx++) {
                        const nx = x + cx;
                        const ny = y + cy;
                        if (nx < width && ny < height) {
                            const nIdx = 3 * layerSize + (ny * width + nx);
                            // 水晶(ゴール)を上書きしないように（IDチェックは難しいが、端っこなら避ける）
                            if (nx > width - 3 || ny > height - 3) continue;
                            mapData.data[nIdx] = tile;
                        }
                    }
                }
            }
        }
    }

    fs.writeFileSync(filepath, JSON.stringify(mapData, null, 2), 'utf8');
}

Object.keys(COMPLEXITY_SETTINGS).forEach(id => {
    refineMap(parseInt(id), COMPLEXITY_SETTINGS[id]);
});

console.log("Map complexity refinement complete!");
