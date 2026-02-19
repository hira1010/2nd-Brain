const fs = require('fs');
const path = require('path');

const ROOT_DIR = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\18_レミ投資漫画";
const ARCHIVE_DIR = path.join(ROOT_DIR, "99_知識保管庫");
const TARGET_FOLDERS = [
    "01_投資の基礎知識",
    "02_マインド・哲学",
    "03_戦略・リスク管理",
    "04_未来・テクノロジー"
];

function moveFolder(src, dest) {
    if (!fs.existsSync(src)) {
        console.log(`Not found: ${src}`);
        return;
    }

    // If destination folder doesn't exist, just rename src to dest.
    if (!fs.existsSync(dest)) {
        try {
            fs.renameSync(src, dest);
            console.log(`Moved: ${path.basename(src)} -> 99_知識保管庫`);
        } catch (e) {
            console.error(`Error moving ${src}: ${e.message}`);
        }
        return;
    }

    // If destination DOES exist, we need to move contents.
    console.log(`Merging contents of ${src} into ${dest}`);
    const files = fs.readdirSync(src);
    for (const file of files) {
        const s = path.join(src, file);
        const d = path.join(dest, file);

        if (fs.existsSync(d)) {
            console.log(`Skipping duplicate: ${file}`);
        } else {
            try {
                fs.renameSync(s, d);
            } catch (e) {
                console.error(`Error moving file ${file}: ${e.message}`);
            }
        }
    }

    // Remove empty src dir
    try {
        fs.rmdirSync(src);
        console.log(`Removed empty source: ${src}`);
    } catch (e) {
        console.error(`Could not remove source (not empty?): ${e.message}`);
    }
}

function main() {
    if (!fs.existsSync(ARCHIVE_DIR)) {
        fs.mkdirSync(ARCHIVE_DIR);
        console.log("Created archive directory.");
    }

    for (const folder of TARGET_FOLDERS) {
        moveFolder(path.join(ROOT_DIR, folder), path.join(ARCHIVE_DIR, folder));
    }
}

main();
