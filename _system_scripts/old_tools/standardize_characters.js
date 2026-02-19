const fs = require('fs');
const path = require('path');

const rootDir = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\18_レミ投資漫画";
const newBlock = `### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel).`;

function walkDir(dir, callback) {
    try {
        fs.readdirSync(dir).forEach(f => {
            let dirPath = path.join(dir, f);
            let isDirectory = fs.statSync(dirPath).isDirectory();
            if (isDirectory) {
                walkDir(dirPath, callback);
            } else {
                callback(path.join(dir, f));
            }
        });
    } catch (e) {
        console.error(`Error reading directory ${dir}: ${e.message}`);
    }
}

let count = 0;

console.log("Starting batch update...");

walkDir(rootDir, (filePath) => {
    if (filePath.endsWith('プロンプト.md')) {
        try {
            let content = fs.readFileSync(filePath, 'utf8');
            
            // 1. Remove existing Character blocks to avoid duplicates/inconsistencies.
            //    Regex matches:
            //    start of line (conceptually), ### Characters:, followed by newlines
            //    - Remi: ... (multiline match via [\s\S]*?)
            //    - Yuto: ... (ending at newline)
            //    We match specifically Remi then Yuto order to catch the standard block.
            let removeRegex = /### Characters:\s*[\r\n]+\s*- Remi:[\s\S]*?- Yuto:[^\r\n]*(\r?\n)+/g;
            let cleanContent = content.replace(removeRegex, '');

            // 2. Insert the standard definition block after every ARCHITECTURE line.
            //    This ensures every page (that has an ARCHITECTURE line) gets the characters.
            let insertRegex = /^(ARCHITECTURE:.*)$/gm;
            let finalContent = cleanContent.replace(insertRegex, (match) => {
                return match + "\n\n" + newBlock;
            });

            if (finalContent !== content) {
                fs.writeFileSync(filePath, finalContent, 'utf8');
                console.log(`Updated: ${path.basename(filePath)}`);
                count++;
            }
        } catch (e) {
            console.error(`Error processing ${filePath}: ${e.message}`);
        }
    }
});

console.log(`Total files updated: ${count}`);
