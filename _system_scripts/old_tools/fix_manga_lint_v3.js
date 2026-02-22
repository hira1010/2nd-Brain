const fs = require('fs');
const path = require('path');

/**
 * fix_manga_lint_v3.js
 * 目的: MD022 (Headings around blank lines), MD032 (Lists around blank lines), MD040 (Code block lang) の修正
 */

function fixContent(content) {
    let lines = content.split(/\r?\n/);
    let newLines = [];
    let modified = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let nextLine = lines[i + 1] !== undefined ? lines[i + 1] : null;
        let prevLine = newLines.length > 0 ? newLines[newLines.length - 1] : null;

        // MD040: 言語タグのないコードブロックの修正 (v2から継承)
        if (line.trim() === '```') {
            if (nextLine && nextLine.trim() !== '```') {
                if (nextLine.match(/^(generate_image\(|const |let |var |function |#|if |for |while |import |export )/)) {
                    line = '```javascript';
                    modified = true;
                } else if (nextLine.match(/^(FORMAT:|SIZE:|Characters:|### |\[Panel |Technical Style:)/)) {
                    line = '```text';
                    modified = true;
                } else if (nextLine.trim() !== "") {
                    line = '```text';
                    modified = true;
                }
            }
        }

        // MD022: 見出し (#, ##, ###) の前に空行を挿入
        if (line.match(/^#+ /) && prevLine !== null && prevLine.trim() !== "" && !prevLine.startsWith("<!--")) {
            newLines.push("");
            modified = true;
        }

        // --- の前後にも空行を入れる（見出しとの境界でエラーになりやすいため）
        if (line.trim() === '---') {
            if (prevLine !== null && prevLine.trim() !== "") {
                newLines.push("");
                modified = true;
            }
        }

        newLines.push(line);

        // MD022/MD032: 見出しや --- の後に、リストや次の要素が続く場合に空行を挿入
        if (line.match(/^#+ /) || line.trim() === '---') {
            if (nextLine !== null && nextLine.trim() !== "" && !nextLine.match(/^#+ /) && !nextLine.trim().startsWith("---")) {
                newLines.push("");
                modified = true;
            }
        }

        // MD032: リスト (- ) の前に空行がない場合 (前の行が空行でも見出しでもない場合)
        if (line.match(/^[-*] /)) {
            // nextLine ではなく、current line がリストの場合の「前」をチェック
            // ただし、既に上で push(line) してしまっているので、newLines の最後から2番目を調整するのは難しい。
            // 処理順序を考慮して、以下のように「前」をチェックする
        }
    }

    // MD032 のための再スキャン (リストの前に空行を入れる)
    let finalLines = [];
    for (let i = 0; i < newLines.length; i++) {
        let line = newLines[i];
        let prev = finalLines[finalLines.length - 1];
        if (line.match(/^[-*] /) && prev !== undefined && prev.trim() !== "" && !prev.match(/^[-*] /)) {
            finalLines.push("");
            modified = true;
        }
        finalLines.push(line);
    }

    return { content: finalLines.join('\n'), modified };
}

function walk(dir) {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat && stat.isDirectory()) {
            if (!['_archive', '.git', 'node_modules', '99_外部ツール'].includes(file)) {
                walk(filePath);
            }
        } else if (file.endsWith('.md')) {
            let content = fs.readFileSync(filePath, 'utf8');
            let result = fixContent(content);

            if (result.modified) {
                fs.writeFileSync(filePath, result.content, 'utf8');
                console.log(`Cleanly Refactored: ${filePath}`);
            }
        }
    });
}

walk('.');
console.log('Advanced MD022/MD032/MD040 Lint fix completed.');
