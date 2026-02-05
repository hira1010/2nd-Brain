import re
import os
import manga_config as config
import manga_utils as utils

from manga_prompt_builder import MangaPromptBuilder

def update_file_with_variation(filepath):
    content = utils.read_file(filepath)
    
    # 1. Parse Metadata using Utils
    meta = utils.parse_metadata(content)
    if 'number' not in meta: return False

    # 2. Use Builder to generate content
    builder = MangaPromptBuilder(meta)
    new_p1_content = builder.build_page1()
    new_p2_content = builder.build_page2()
    
    page_count = builder.page_count

    # ファイルの中身を更新
    new_full_content = content
    
    # 1 page header determination
    p1_header = "## 1ページ目プロンプト" if page_count > 1 else "## プロンプト"
    
    # Replace P1 block (Handling both old and new header styles)
    # Match ## 1ページ目プロンプト OR ## プロンプト
    p1_pattern = r'## (1ページ目プロンプト|プロンプト)\s*\n\s*```text\s*\n(.*?)\n```'
    
    # Replacement string
    p1_replacement = f"{p1_header}\n\n```text\n{new_p1_content}\n```"
    
    if re.search(p1_pattern, new_full_content, flags=re.DOTALL):
        new_full_content = re.sub(p1_pattern, p1_replacement, new_full_content, flags=re.DOTALL)
    else:
        # If not found, append? (Unlikely for existing files)
        pass

    # Replace P2 block
    p2_pattern = r'## 2ページ目プロンプト\s*\n\s*```text\s*\n(.*?)\n```'
    
    if page_count > 1:
        if new_p2_content:
            p2_replacement = f"## 2ページ目プロンプト\n\n```text\n{new_p2_content}\n```"
            if re.search(p2_pattern, new_full_content, flags=re.DOTALL):
                new_full_content = re.sub(p2_pattern, p2_replacement, new_full_content, flags=re.DOTALL)
            else:
                # If page 2 is missing but requested, better to append it after P1?
                # For now, let's assume structure exists if page_count > 1.
                # If it doesn't match, we might need to insert it.
                # Simplification: Only split if it exists.
                pass
    else:
        # Page count 1: Remove P2 if it exists
        new_full_content = re.sub(p2_pattern, "", new_full_content, flags=re.DOTALL)
        
        # Cleanup extra newlines created by removal
        new_full_content = re.sub(r'\n\s*\n\s*\n', '\n\n', new_full_content)

    if new_full_content != content:
        utils.write_file(filepath, new_full_content)
        return True
    return False

if __name__ == "__main__":
    count = 0
    for filepath in utils.find_manga_prompt_files(config.BASE_DIR):
        if update_file_with_variation(filepath):
            count += 1
    print(f"Updated {count} files with variations.")
