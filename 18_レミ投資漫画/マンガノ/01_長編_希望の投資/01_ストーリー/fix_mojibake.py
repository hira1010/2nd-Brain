import sys
import os

def fix_line(line):
    # Check if line contains common garbled char lead byte representation in SJIS->UTF8
    # '縺' is E3 81 (Lead byte E3, Trailing 81).
    if '縺' not in line and '蜈' not in line and '蜆' not in line:
        return line

    try:
        # The key transformation:
        # The text was UTF-8 bytes, interpreted as CP932, then saved as UTF-8.
        # So we reverse:
        # 1. Encode back to CP932 (to recover the original UTF-8 bytes)
        # 2. Decode as UTF-8 (to get the original text)
        
        # We use 'ignore' to skip bytes that cannot be mapped back to CP932 (e.g. if they were replaced by '?' or '・')
        raw_bytes = line.encode('cp932', errors='ignore')
        
        # We use 'replace' to handle any bytes that were recovered but don't form valid UTF-8
        fixed = raw_bytes.decode('utf-8', errors='replace')
        
        # Heuristic: If fixed looks like valid Japanese, return it.
        # Otherwise return original.
        return fixed
    except Exception as e:
        # print(f"Failed to fix line: {e}")
        return line

def process_file(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        changed = False
        for line in lines:
            fixed = fix_line(line)
            if fixed != line:
                # print(f" Original: {line.strip()}")
                # print(f" Fixed:    {fixed.strip()}")
                changed = True
            fixed_lines.append(fixed)
            
        if changed:
            new_path = filepath + ".fixed"
            with open(new_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            print(f"Created {new_path}")
            # print("Preview of first 5 changed lines:")
            # for i in range(min(5, len(lines))):
            #     if lines[i] != fixed_lines[i]:
            #         print(f"Original: {lines[i].strip()}")
            #         print(f"Fixed:    {fixed_lines[i].strip()}")
        else:
            print("No changes needed.")
            
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_mojibake.py <file>")
        sys.exit(1)
        
    for f in sys.argv[1:]:
        process_file(f)
