import os
import codecs

def convert_files():
    files = ["generate_mangano.py", "manga_config.py", "manga_utils.py", "fix_manga_prompts.py"]
    base_dir = os.getcwd()
    
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            try:
                # Read as utf-8 (assuming they are currently utf-8 without BOM or with BOM)
                # First try utf-8-sig to handle if it already has BOM
                try:
                    with codecs.open(filepath, "r", "utf-8-sig") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # Fallback to utf-8
                    with codecs.open(filepath, "r", "utf-8") as f:
                        content = f.read()
                
                # Write back as utf-8-sig
                with codecs.open(filepath, "w", "utf-8-sig") as f:
                    f.write(content)
                print(f"Converted {filename} to UTF-8 with BOM")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    convert_files()
