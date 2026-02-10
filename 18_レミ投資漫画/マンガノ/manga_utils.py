# -*- coding: utf-8 -*-
import os

def ensure_directory(path):
    """Ensure that the directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def save_text_file(filepath, content, encoding='utf-8'):
    """Save content to a text file."""
    try:
        with open(filepath, "w", encoding=encoding) as f:
            f.write(content)
        print(f"Saved: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def load_text_file(filepath, encoding='utf-8'):
    """Load content from a text file."""
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def get_episode_filename(episode, base_dir):
    """Generate the filename for an episode."""
    title_escaped = episode['title'].replace('/', '_').replace(' ', '_')
    filename = f"No102_{episode['no']:02d}_{title_escaped}_{episode['range']}_プロンプト.md"
    return os.path.join(base_dir, filename)
