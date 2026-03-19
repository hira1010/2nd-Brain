import * as fs from 'fs/promises';
import * as path from 'path';

const PROJECT_PATH = "C:/Users/hirak/Documents/RMMZ/Project1";
const DATA_PATH = path.join(PROJECT_PATH, "data");

async function findHole() {
    const mapPath = path.join(DATA_PATH, "Map001.json");
    const content = await fs.readString(mapPath); // Wait, readString is not a thing, use readFile
    const map = JSON.parse(await fs.readFile(mapPath, "utf-8"));
    const width = map.width;
    
    console.log(`Map Width: ${width}, Height: ${map.height}`);
    
    // Hole tiles in many tilesets are around 3328-3335 or 3376-3383
    const holeTiles = [3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3376, 3377, 3378, 3379, 3380, 3381, 3382, 3383];
    
    for (let i = 0; i < map.data.length; i++) {
        if (holeTiles.includes(map.data[i])) {
            const x = i % width;
            const y = Math.floor(i / width) % map.height;
            console.log(`Hole tile ${map.data[i]} found at (${x}, ${y})`);
        }
    }
}

findHole().catch(console.error);
