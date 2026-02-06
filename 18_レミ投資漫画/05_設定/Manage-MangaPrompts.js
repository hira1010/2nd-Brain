const fs = require('fs');
const path = require('path');

/** 
 * MangaSystem Engine v3.2
 * Added: Short Keyword Extraction for stable Japanese rendering
 * Fixed: NO hardcoded theme-bias in templates
 */

const scriptDir = __dirname;
const jsonPath = path.join(scriptDir, 'prompt_data.json');
const parentDir = path.resolve(scriptDir, '..');

const cfg = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

/**
 * Extracts a short, high-impact Japanese keyword for DALL-E to render safely.
 */
function getShortKeyword(text, index) {
    if (!text) return "真実！";
    // Remove symbols
    let clean = text.replace(/[！、。？！『』「」]/g, '');
    let parts = clean.split(/[ \n\t]/);
    let target = parts[index % parts.length] || parts[0];

    // Take first 4-5 chars if too long
    return target.substring(0, 5) + "！";
}

function buildPrompt(title, desc, isSpiritual, pageNum) {
    const remi = cfg.characters.remi;
    const yuto = cfg.characters.yuto;
    const anatomy = cfg.styles.anatomy;
    const titleBox = cfg.layout.title_box.split('{Title}').join(title);

    const kw1 = getShortKeyword(title, 0);
    const kw2 = getShortKeyword(desc, 0);

    const header = cfg.templates.common_header
        .split('{Remi}').join(remi)
        .split('{Yuto}').join(yuto)
        .split('{Anatomy}').join(anatomy);

    const baseTpl = isSpiritual ? cfg.templates.spiritual : cfg.templates.normal;
    const pKey = `p${pageNum}`;
    const bodyParts = baseTpl[pKey] || baseTpl.p1;

    let body = bodyParts.map(p => {
        return p.split('{TitleBox}').join(pageNum === 1 ? titleBox : "")
            .split('{Title}').join(title)
            .split('{Desc}').join(desc)
            .split('{Keyword1}').join(kw1)
            .split('{Keyword2}').join(kw2);
    }).join('\n');

    body = body.replace(/  \n/g, "\n");
    const footer = cfg.templates.footer;

    return cfg.styles.global_prefix + "\n\n" + header + body + footer;
}

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            if (!['_archive', '.git', 'node_modules', '99_外部ツール'].includes(file)) {
                results = results.concat(walk(filePath));
            }
        } else if (file.startsWith('No') && file.endsWith('.md')) {
            results.push(filePath);
        }
    });
    return results;
}

const targetFiles = walk(parentDir);
let count = 0;

targetFiles.forEach(f => {
    try {
        let content = fs.readFileSync(f, 'utf8');
        const originalContent = content;

        const noMatch = content.match(/\| No \| (\d+) \|/);
        const no = noMatch ? parseInt(noMatch[1]) : 0;

        const titleMatch = content.match(new RegExp(cfg.logic.TitleRegex));
        const title = titleMatch ? titleMatch[1].trim() : "Invest";

        const descMatch = content.match(new RegExp(cfg.logic.DescRegex));
        const desc = descMatch ? descMatch[1].trim() : "Desc";

        const isSpiritual = (no > 0 && no % 3 === 0);

        for (let i = 1; i <= 4; i++) {
            const masterPrompt = buildPrompt(title, desc, isSpiritual, i);

            // 1. プロンプト本文の更新
            const pageRegex = new RegExp(`(## .*?${i}.*?\\n\\s*\`\`\`text\\s*\\n)[\\s\\S]*?(\\n\`\`\`)`);
            if (content.match(pageRegex)) {
                content = content.replace(pageRegex, `$1${masterPrompt}$2`);
            }

            // 2. generate_image 呼び出し例の更新（Size 1024x1792 を追加）
            const genRegex = new RegExp(`(generate_image\\(\\s*ImageName: ".*?",\\s*Prompt: \\[.*?\\])(\\s*\\))`, 'g');
            content = content.replace(genRegex, `$1,\n  Size: "1024x1792"$2`);
        }

        if (content !== originalContent) {
            fs.writeFileSync(f, content, 'utf8');
            count++;
            process.stdout.write('.');
        }
    } catch (err) {
        console.error(`\nError in ${f}: ${err}`);
    }
});

console.log(`\n\n[SUCCESS] Updated ${count} files with Vertical Size Support (1024x1792) and Masker Standard.`);
