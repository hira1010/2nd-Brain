import os

def search_text(root_dir, target_text):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.json') or file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if target_text in f.read():
                            print(f"FOUND in: {path}")
                except Exception:
                    pass

search_text('c:/Users/hirak/Desktop/2nd-Brain', '近づいてきてます')
search_text('c:/Users/hirak/Desktop/2nd-Brain', '仮想通貨マン')
