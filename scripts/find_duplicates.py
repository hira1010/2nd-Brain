import os
import unicodedata

def find_duplicates(root_dir):
    items = os.listdir(root_dir)
    dirs = [item for item in items if os.path.isdir(os.path.join(root_dir, item))]
    
    nfc_map = {}
    duplicates = []
    
    # Check for Unicode normalization duplicates
    for d in dirs:
        nfc_name = unicodedata.normalize('NFC', d)
        if nfc_name in nfc_map:
            duplicates.append((nfc_map[nfc_name], d))
        else:
            nfc_map[nfc_name] = d
            
    # Check for index number duplicates (e.g., 01_, 02_)
    index_map = {}
    index_duplicates = []
    for d in dirs:
        if '_' in d:
            parts = d.split('_', 1)
            prefix = parts[0]
            if prefix.isdigit():
                if prefix in index_map:
                    index_duplicates.append((index_map[prefix], d))
                else:
                    index_map[prefix] = d
                    
    return duplicates, index_duplicates

root = r'C:\Users\hirak\Desktop\2nd-Brain'
dupes, index_dupes = find_duplicates(root)

output_file = r'C:\Users\hirak\Desktop\2nd-Brain\scripts\duplicates_report.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("--- Unicode Normalization Duplicates ---\n")
    for d1, d2 in dupes:
        f.write(f"'{d1}' and '{d2}'\n")

    f.write("\n--- Index Number Duplicates ---\n")
    for d1, d2 in index_dupes:
        f.write(f"'{d1}' and '{d2}'\n")

