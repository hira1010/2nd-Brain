const fs = require('fs');
const path = require('path');

const TARGET_DIR = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\18_レミ投資漫画";

// Master Definitions
const MASTER_ARCHITECTURE = "ARCHITECTURE: [v15.5 EDGE OBLITERATOR] FULL BLEED. ZERO PIXEL MARGINS. 110% OVERFILL. 12:17.";
const MASTER_REMI = "- Remi: (Crimson RED blazer, Black lace top). (LONG STARK STRAIGHT SILVER hair). (GLOWING SOLID BLOOD-RED eyes). NO GLOVES.";
const MASTER_YUTO = "- Yuto: (BLACK Gakuran, gold buttons). (Short Black hair). BARE HANDS.";
// Added "best quality, masterpiece, sharp focus" to Style to assist with face consistency
const MASTER_STYLE = "### Style: Premium manga, cinematic lighting, best quality, masterpiece, sharp focus, high contrast. 12:17 ratio. **CORE**: OBLITERATE ALL CANVAS MARGINS. ALL ART MUST BE FULL BLEED.";
const MASTER_NEGATIVE = "**NEGATIVE PROMPT**: white edges, side bars, pillarbox, letterbox, black bars, gutter, split screen, frame, border, text labels, low quality, blurry, margins, padding, cropped.";

function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;

    // 1. Replace ARCHITECTURE block up to "### Characters"
    content = content.replace(
        /ARCHITECTURE:[\s\S]*?### Characters:/g,
        `${MASTER_ARCHITECTURE} ### Characters:`
    );

    // 2. Replace Remi Definition
    content = content.replace(
        /- Remi:[\s\S]*?(?=- Yuto)/g,
        `${MASTER_REMI}\n`
    );

    // 3. Replace Yuto Definition
    content = content.replace(
        /- Yuto:[\s\S]*?(?=\[PANEL)/g,
        `${MASTER_YUTO}\n\n`
    );

    // 4. Replace Style Section
    // Matches "### Style:" until "**NEGATIVE PROMPT**"
    content = content.replace(
        /### Style:[\s\S]*?(?=\*\*NEGATIVE)/g,
        `${MASTER_STYLE}\n`
    );

    // 5. Update/Replace Negative Prompt
    // Matches "**NEGATIVE PROMPT**: ... (until end of quote)"
    content = content.replace(
        /\*\*NEGATIVE PROMPT\*\*:[\s\S]*?(?=")/g,
        `${MASTER_NEGATIVE}`
    );

    if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Updated: ${path.basename(filePath)}`);
    }
}

function traverseDir(dir) {
    if (!fs.existsSync(dir)) {
        console.log(`Directory not found: ${dir}`);
        return;
    }
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            traverseDir(fullPath);
        } else if (file.endsWith('_プロンプト.md')) {
            processFile(fullPath);
        }
    }
}

console.log("Starting Aggressive Master Fix...");
traverseDir(TARGET_DIR);
console.log("Completed Aggressive Master Fix.");
