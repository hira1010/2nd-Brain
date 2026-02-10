# -*- coding: utf-8 -*-
import os
from typing import Dict, Optional, Tuple


def ensure_directory(path: str) -> None:
    """Ensure that the directory exists."""
    if os.path.exists(path):
        return
    os.makedirs(path)
    print(f"Created directory: {path}")


def _to_safe_title(text: str) -> str:
    return text.replace("/", "_").replace(" ", "_")


def parse_page_range(page_range: str) -> Tuple[int, int]:
    """Parse page range like 'P1-5' into (1, 5)."""
    start_text, end_text = page_range.split("-", 1)
    start_page = int(start_text.replace("P", ""))
    end_page = int(end_text)
    return start_page, end_page


def save_text_file(filepath: str, content: str, encoding: str = "utf-8") -> bool:
    """Save content to a text file."""
    try:
        with open(filepath, "w", encoding=encoding) as f:
            f.write(content)
        print(f"Saved: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def load_text_file(filepath: str, encoding: str = "utf-8") -> Optional[str]:
    """Load content from a text file."""
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def get_episode_filename(episode: Dict[str, object], base_dir: str) -> str:
    """Generate the filename for an episode."""
    title_escaped = _to_safe_title(str(episode["title"]))
    filename = (
        f"No102_{int(episode['no']):02d}_{title_escaped}_{episode['range']}_繝励Ο繝ｳ繝励ヨ.md"
    )
    return os.path.join(base_dir, filename)
