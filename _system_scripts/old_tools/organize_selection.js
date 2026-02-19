const fs = require('fs');
const path = require('path');

const ROOT_DIR = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\18_レミ投資漫画";

const CHAPTER_MAP = {
    1: "01_現状把握と脱労働",
    2: "02_投資の魔法と基礎",
    3: "03_実践と準備",
    4: "04_継続の技術",
    5: "05_投資の果実と自由"
};

const TITLE_KEYWORDS = {
    1: "配当貴族"
};

function parseSelectionList() {
    const selectionFile = path.join(ROOT_DIR, "05_設定", "初心者向け連載30選.md");
    const selections = [];
    let currentChapter = 0;

    try {
        const content = fs.readFileSync(selectionFile, 'utf8');
        const lines = content.split(/\r?\n/);

        for (const line of lines) {
            const chapMatch = line.match(/^## 第(\d+)章/);
            if (chapMatch) {
                currentChapter = parseInt(chapMatch[1], 10);
                continue;
            }

            if (!line.trim().startsWith('|')) continue;

            const parts = line.split('|').map(p => p.trim());
            if (parts.length < 4) continue;

            const noStr = parts[1];
            const titleStr = parts[2];

            if (!/^\d+$/.test(noStr)) continue;

            const no = parseInt(noStr, 10);
            const title = titleStr.replace(/\*/g, '').trim();

            selections.push({
                chapter: currentChapter,
                no: no,
                title: title
            });
        }
    } catch (e) {
        console.error(`Error reading selection list: ${e.message}`);
    }
    return selections;
}

function findFile(no, titleKeyword) {
    let found = [];

    function walk(dir) {
        const files = fs.readdirSync(dir);
        for (const f of files) {
            const fullPath = path.join(dir, f);
            const stat = fs.statSync(fullPath);
            if (stat.isDirectory()) {
                walk(fullPath);
            } else {
                // Check pattern: NoXX_*プロンプト.md or similar
                // We need to be careful. Let's look for "No" + numbers + something + "プロンプト.md"
                // The python script used: f"No{item['no']:02d}_*プロンプト.md"
                // JS regex: /No(0?1)_.*プロンプト\.md/

                // Construct regex for this specific No
                // valid formats: No1_..., No01_..., No.1_...
                // We'll stick to simple check: file starts with No+number

                // Matches "No" followed by the number (with optional 0 padding) and a non-digit
                // e.g. for No=1: No01_..., No1_...
                const nameHelper = `No${no.toString().padStart(2, '0')}_`;
                const nameHelper2 = `No${no}_`;

                if ((f.startsWith(nameHelper) || f.startsWith(nameHelper2)) && f.endsWith('プロンプト.md')) {
                    // If keyword restriction exists
                    if (titleKeyword) {
                        if (!f.includes(titleKeyword)) return;
                    }
                    found.push(fullPath);
                }
            }
        }
    }

    try {
        walk(ROOT_DIR);
    } catch (e) {
        console.error(`Error walking directory: ${e.message}`);
    }
    return found;
}

function main() {
    console.log("Starting organization...");
    const selections = parseSelectionList();
    console.log(`Loaded ${selections.length} episodes.`);

    // Ensure target dirs exist
    for (const key in CHAPTER_MAP) {
        const targetDir = path.join(ROOT_DIR, CHAPTER_MAP[key]);
        if (!fs.existsSync(targetDir)) {
            fs.mkdirSync(targetDir, { recursive: true });
            console.log(`Created dir: ${CHAPTER_MAP[key]}`);
        }
    }

    let movedCount = 0;

    for (const item of selections) {
        const targetFolderName = CHAPTER_MAP[item.chapter];
        if (!targetFolderName) {
            console.warn(`Unknown chapter ${item.chapter} for No.${item.no}`);
            continue;
        }

        const targetDir = path.join(ROOT_DIR, targetFolderName);
        const keyword = TITLE_KEYWORDS[item.no];

        let candidates = findFile(item.no, keyword);

        if (candidates.length === 0) {
            console.log(`File NOT FOUND for No.${item.no} (${item.title})`);
            continue;
        }

        let srcPath = candidates[0];
        // If multiple, try to match title
        if (candidates.length > 1) {
            const exactMatch = candidates.find(c => path.basename(c).includes(item.title));
            if (exactMatch) srcPath = exactMatch;
        }

        const fileName = path.basename(srcPath);
        const destPath = path.join(targetDir, fileName);

        if (path.resolve(srcPath) === path.resolve(destPath)) {
            console.log(`Already in place: ${fileName}`);
            continue;
        }

        try {
            fs.renameSync(srcPath, destPath);
            console.log(`MOVED: ${fileName} -> ${targetFolderName}`);
            movedCount++;
        } catch (e) {
            console.error(`ERROR moving ${fileName}: ${e.message}`);
        }
    }

    console.log(`\nDone. Moved ${movedCount} files.`);
}

main();
