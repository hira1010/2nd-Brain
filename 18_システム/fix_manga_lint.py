#!/usr/bin/env python3
"""
漫画プロンプトファイルの完全修正スクリプト

すべてのMarkdown Lintエラーを修正:
- MD032: Lists should be surrounded by blank lines
- MD022: Headings should be surrounded by blank lines  
- その他のフォーマット問題
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画")

def fix_markdown(content: str) -> str:
    """Markdownを完全に修正"""
    lines = content.splitlines()
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        prev_line = lines[i-1] if i > 0 else ""
        next_line = lines[i+1] if i < len(lines) - 1 else ""
        
        # 見出しの前に空白行を追加
        if line.startswith('#'):
            if prev_line.strip() != "" and not prev_line.startswith('#'):
                result.append("")
        
        # 現在の行を追加
        result.append(line)
        
        # 見出しの後に空白行を追加（ただし次が特殊要素でない場合）
        if line.startswith('#'):
            if next_line.strip() != "" and not next_line.startswith('#') and not next_line.startswith('```') and not next_line.startswith('|') and not next_line.startswith('>'):
                result.append("")
        
        # リストの前に空白行を追加
        is_list = line.strip().startswith('-') or line.strip().startswith('*') or re.match(r'^\s*\d+\.', line.strip())
        prev_is_list = prev_line.strip().startswith('-') or prev_line.strip().startswith('*') or re.match(r'^\s*\d+\.', prev_line.strip())
        
        if is_list and not prev_is_list and prev_line.strip() != "":
            # リストの開始前に空白行がない場合、挿入
            if len(result) >= 2 and result[-2].strip() != "":
                result.insert(-1, "")
        
        i += 1
    
    # 連続する空白行を1つに
    final = []
    prev_empty = False
    for line in result:
        if line.strip() == "":
            if not prev_empty:
                final.append(line)
            prev_empty = True
        else:
            final.append(line)
            prev_empty = False
    
    return '\n'.join(final)


def main():
    print("=" * 70)
    print("漫画プロンプト Markdown Lint 完全修正")
    print("=" * 70)
    
    files = list(BASE_DIR.rglob("*プロンプト.md"))
    print(f"\n対象ファイル: {len(files)}件\n")
    
    fixed = 0
    for file_path in sorted(files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original = f.read()
            
            modified = fix_markdown(original)
            
            if modified != original:
                with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(modified)
                print(f"✓ {file_path.name}")
                fixed += 1
            else:
                print(f"- {file_path.name} (変更なし)")
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
    
    print(f"\n{'=' * 70}")
    print(f"完了: {fixed}/{len(files)} ファイル修正")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
