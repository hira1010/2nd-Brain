const fs = require('fs');
const path = require('path');

function walk(dir) {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat && stat.isDirectory()) {
            if (!['_archive', '.git', 'node_modules'].includes(file)) {
                walk(filePath);
            }
        } else if (file.endsWith('.md')) {
            let content = fs.readFileSync(filePath, 'utf8');
            let originalContent = content;

            /**
             * 強力な置換ロジック:
             * 言語指定のない ``` (直後に改行) を探し、
             * 続く数行のパターンによって javascript か text を付与する。
             */

            // 1. 既に言語指定があるものは無視
            // 2. 言語指定のない ``` を見つける
            let lines = content.split(/\r?\n/);
            let modified = false;

            for (let i = 0; i < lines.length; i++) {
                if (lines[i].trim() === '```') {
                    // 次の行を見て、言語タグが必要か判断
                    let nextLine = lines[i + 1] || "";

                    // 次の行が既に閉じ括弧 ``` なら無視
                    if (nextLine.trim() === '```') continue;

                    // コンテンツに応じた言語推測
                    if (nextLine.match(/^(generate_image\(|const |let |var |function |#|if |for |while |import |export )/)) {
                        lines[i] = '```javascript';
                        modified = true;
                    } else if (nextLine.match(/^(FORMAT:|SIZE:|Characters:|### |\[Panel |Technical Style:)/)) {
                        lines[i] = '```text';
                        modified = true;
                    } else if (nextLine.trim() !== "") {
                        // 何らかのコンテンツがある場合はデフォルトで text を付与 (MD040 回避のため)
                        lines[i] = '```text';
                        modified = true;
                    }
                }
            }

            if (modified) {
                fs.writeFileSync(filePath, lines.join('\n'), 'utf8');
                console.log(`Fully Fixed: ${filePath}`);
            }
        }
    });
}

walk('.');
console.log('Advanced Lint fix completed.');
