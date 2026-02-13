# -*- coding: utf-8 -*-
import os
import sys
from typing import Dict, Optional, Tuple, List

# Standard encodings to try for Japanese Windows environment
ENCODINGS = ["utf-8", "cp932", "shift_jis", "utf-8-sig"]

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
    if not page_range:
        return 0, 0
    try:
        start_text, end_text = page_range.split("-", 1)
        start_page = int(start_text.replace("P", ""))
        end_page = int(end_text)
        return start_page, end_page
    except ValueError:
        return 0, 0


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


def load_text_file(filepath: str) -> Optional[str]:
    """
    Load content from a text file, trying multiple encodings.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    for enc in ENCODINGS:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error loading {filepath} with {enc}: {e}")
            continue
    
    print(f"Failed to load {filepath} with any encoding: {ENCODINGS}")
    return None


def get_episode_filename(episode: Dict[str, object], base_dir: str) -> str:
    """Generate the filename for an episode."""
    title_escaped = _to_safe_title(str(episode["title"]))
    # Use proper Japanese prompt suffix
    filename = (
        f"No102_{int(episode['no']):02d}_{title_escaped}_{episode['range']}_プロンプト.md"
    )
    return os.path.join(base_dir, filename)

def setup_console_encoding():
    """Ensure stdout handles utf-8 for Windows consoles"""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
