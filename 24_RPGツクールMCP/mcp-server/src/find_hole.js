const fs = require('fs');
const path = require('path');

const mapPath = "C:/Users/hirak/Documents/RMMZ/Project1/data/Map001.json";
const map = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
const width = map.width;

const holeTiles = [3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3376, 3377, 3378, 3379, 3380, 3381, 3382, 3383];

console.log(`WIDTH: ${width}`);
map.data.forEach((tile, i) => {
    if (holeTiles.includes(tile)) {
        const x = i % width;
        const y = Math.floor(i / (width));
        // There are multiple layers in data, so y can go beyond height. RMMZ uses 6 layers.
        const layer = Math.floor(y / map.height);
        const actualY = y % map.height;
        console.log(`TILE: ${tile} at (${x}, ${actualY}) Layer: ${layer}`);
    }
});
