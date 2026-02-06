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

            // 言語指定のないコードブロックの開始を探す
            // 具体的なコンテンツが後に続く場合にのみ、javascript または text を追加する
            // 1. generate_image などのコード例
            content = content.replace(/^```\r?\n(generate_image\(|const |let |var |function |#|if |for |while )/gm, '```javascript\n$1');

            // 2. プロンプト本文などのテキスト（FORMAT:, SIZE: など）
            content = content.replace(/^```\r?\n(FORMAT:|SIZE:|Characters:|### )/gm, '```text\n$1');

            if (content !== originalContent) {
                fs.writeFileSync(filePath, content, 'utf8');
                console.log(`Fixed: ${filePath}`);
            }
        }
    });
}

walk('.');
console.log('Lint fix completed.');
