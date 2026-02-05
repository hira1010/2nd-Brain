import os
import re

def find_manga_prompt_files(base_dir):
    """
    Generator that yields the absolute path of all files ending with '_プロンプト.md'
    within the given base_dir (recursive).
    """
    for root, dirs, files in os.walk(base_dir):
        for name in files:
            if name.endswith("_プロンプト.md"):
                yield os.path.join(root, name)

def read_file(filepath):
    """Reads file content with utf-8 encoding."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Writes content to file with utf-8 encoding."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def parse_metadata(content):
    """Parses markdown content to extract TIP information and Dialogues."""
    data = {}
    
    # Extract TIP Info table
    # | 項目 | 内容 | ... | No | 28 | ...
    # Simple regex for table rows
    table_pattern = r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|'
    matches = re.findall(table_pattern, content)
    
    key_map = {
        'No': 'number',
        'タイトル': 'title',
        '解説': 'description',
        'カテゴリー': 'category',
        'TIP_NUMBER': 'number',
        'TIP_TITLE': 'title',
        'DIALOGUE_INTRO': 'dialogue_intro',
        'DIALOGUE_TEACH': 'dialogue_teach',
        'DIALOGUE_DESC': 'dialogue_desc',
        'DIALOGUE_ACTION': 'dialogue_action',
        'ページ数': 'page_count'
    }
    
    for key, val in matches:
        key = key.strip()
        val = val.strip()
        if key in key_map:
            # First match wins usually, but for tables in different sections, we confuse them.
            # The files have "TIP情報" table and "生成時の変数一覧" tables.
            # Usually "解説" is in TIP info. Dialogues are in variables.
            # We just merge them.
            data[key_map[key]] = val
            
    # Default fallbacks
    data.setdefault('dialogue_intro', 'レミさん！教えてください！')
    data.setdefault('dialogue_teach', 'いいわよ。しっかり聞きなさい。')
    data.setdefault('dialogue_desc', data.get('description', 'これが投資の本質よ。'))
    data.setdefault('dialogue_action', 'なるほど！実践してみます！')
    
    # Clean up generic technical text if accidentally captured
    if data['dialogue_teach'] == 'Description': data['dialogue_teach'] = 'いいわよ。' 

    return data
