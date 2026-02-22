const fs = require('fs');
const path = require('path');

/** 
 * MangaSystem Engine v6.5 (Refactor Edition)
 * Updated: v6.5 Standard (High-quality Cel Shading, Side-swept Bangs, Script Section)
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
    let clean = text.replace(/[！、。？！『』「」]/g, '');
    let parts = clean.split(/[ \n\t]/);
    let target = parts[index % parts.length] || parts[0];
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

        // 1. 各ページのプロンプトと生成手順を更新
        for (let i = 1; i <= 4; i++) {
            const masterPrompt = buildPrompt(title, desc, isSpiritual, i);

            // プロンプト本文の更新
            const pageRegex = new RegExp(`(## .*?${i}.*?\\n\\s*\`\`\`text\\s*\\n)[\\s\\S]*?(\\n\`\`\`)`);
            if (content.match(pageRegex)) {
                content = content.replace(pageRegex, `$1${masterPrompt}$2`);
            }

            // generate_image 呼び出し例の言語指定追加 (MD040対策)
            const genLangRegex = new RegExp(`(## .*?${i}.*?手順.*?\\n\\s*\`\`\`)(\\s*\\n\\s*generate_image)`, 'g');
            content = content.replace(genLangRegex, `$1javascript$2`);

            // Size 指定の追加
            const genRegex = new RegExp(`(generate_image\\(\\s*ImageName: ".*?",\\s*Prompt: \\[.*?\\])(\\s*\\))`, 'g');
            content = content.replace(genRegex, `$1,\n  Size: "1024x1792"$2`);
        }

        // 2. キャラクター設定セクションの自動同期
        const charSection = `## キャラクター設定（全ページ共通）

### レミ（Remi）- 厳格に固定
- **髪**: 腰まで届く非常に長いストレートなシルバーヘア、分け目なし（前髪に隙間や分け目の一切ない、重めのパッツン/サイド流しスタイル）
- **目**: 鋭い赤い瞳（ruby red eyes）、長いまつ毛
- **服装**: 深紅のビジネスブレザー（赤いボタン）、白いシャツ、黒レースのインナー（お手本画像通り）
- **体型**: スリムで背が高い大人の女性、エレガントな立ち姿
- **表情**: 知的で自信に満ちた微笑み、冷静

### 優斗（Yuto）- 厳格に固定
- **髪**: 短い黒髪、整った髪型
- **目**: 黒い瞳、純粋な表情
- **服装**: 伝統的な黒い学ラン（gakuran）、立襟、**手袋なし**
- **体型**: 標準的な男子高校生の体型
- **表情**: 好奇心旺盛、真剣に学ぶ姿勢`;

        const charRegex = /## [1-9]?\.? ?キャラクター設定[\s\S]*?(?=---|$|## セリフ|## [1-9]ページ目)/;
        if (content.match(charRegex)) {
            content = content.replace(charRegex, charSection + "\n\n");
        } else {
            content = content.replace(/---/, "---\n\n" + charSection + "\n\n---");
        }

        // 3. セリフ・構成案（台本）セクションの自動挿入
        if (!content.includes('## セリフ・構成案（台本）')) {
            const scriptSection = `## セリフ・構成案（台本）

| ページ | パネル | キャラクター | セリフ・ナレーション |
| :--- | :--- | :--- | :--- |
| 1 | 1 | ナレーション | ${desc} |
| 1 | 2 | レミ | 優斗君、今日の講義は「${title}」よ。 |
| 1 | 3 | 優斗 | よろしくお願いします！ |`;

            content = content.replace(charSection, charSection + "\n\n---\n\n" + scriptSection);
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

console.log(`\n\n[SUCCESS] Refactored ${count} files with v6.5 Master Standard (High-quality Cel Shaded & Scripts).`);
