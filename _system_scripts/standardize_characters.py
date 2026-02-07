import os
import re
import glob

# Define the root directory
ROOT_DIR = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画"

# The standardized character block to insert
NEW_CHARS = """### Characters:
- Remi: (Crimson RED blazer, Black lace top). (Silky SILVER hair), (RED eyes). NO GLOVES. (ONLY ONE Remi per panel).
- Yuto: (Traditional SOLID BLACK Gakuran school uniform, gold buttons). (Short Black hair). BARE HANDS. (ONLY ONE Yuto per panel)."""

# Regex pattern to match the existing Characters block.
# Assumptions:
# 1. Starts with "### Characters:"
# 2. Contains "- Remi:" and "- Yuto:" lines (in that order).
# 3. Ends before a blank line or the start of a panel definition ("[")
# 4. We use re.DOTALL to match content across lines, but we try to be specific about the structure.
PATTERN = r"### Characters:\s*\n\s*- Remi:.*?\n\s*- Yuto:.*?(?=(\n\s*\n|\n\s*\[))"

count = 0
updated_files = 0

print(f"Scanning files in {ROOT_DIR}...")
files = glob.glob(os.path.join(ROOT_DIR, "**", "*プロンプト.md"), recursive=True)
print(f"Found {len(files)} files.")

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Perform substitution
        new_content, n = re.subn(PATTERN, NEW_CHARS, content, flags=re.IGNORECASE | re.DOTALL)
        
        if n > 0 and new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {os.path.basename(filepath)} ({n} pages/sections updated)")
            updated_files += 1
        elif n == 0:
            print(f"Skipped (No match): {os.path.basename(filepath)}")
            # Optional: detailed debug if needed
            # if "Characters:" in content:
            #     print(f"  -> 'Characters:' found but regex failed. Check formatting.")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"\nSummary: Updated {updated_files} files out of {len(files)}.")
