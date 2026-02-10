"""
Manga production system common utilities.
Provides logging, text extraction, and sanitization helper functions.
"""

import logging
import re
from typing import Dict, Optional

_NO_RE = re.compile(r"\|\s*No\s*\|\s*(\d+)\s*\|")
_TITLE_RE = re.compile(r"\|\s*Title\s*\|\s*(.*?)[\s|]*\|", re.IGNORECASE)
_HEADER_TITLE_RE = re.compile(r"#\s*No\.\d+\s+(.*?)($|\s)")
_DESC_RE = re.compile(r"\|\s*Description\s*\|\s*(.*?)[\s|]*\|", re.IGNORECASE)
_INTRO_RE = re.compile(r'Remi says "(.*?)" \(In a speech bubble\)\. Title box:')
_TEACH_RE = re.compile(r'She says "(.*?)" \(In a speech bubble\)\.')
_DETAIL_RE = re.compile(r'She looks gentle and wise\. "(.*?)" \(In a speech bubble\)\.')
_ACTION_RE = re.compile(r'Yuto says "(.*?)" \(In a speech bubble\)\.')
_SAFE_FILENAME_RE = re.compile(r'[\\/*?:"<>|]')

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with a standard format.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logger("manga_utils")

def extract_info_from_md(content: str) -> Dict[str, str]:
    """
    Extracts metadata (No, Title, etc.) from the markdown content.
    """
    info: Dict[str, str] = {}
    
    # Extract No
    no_match = _NO_RE.search(content)
    info['no'] = no_match.group(1) if no_match else "00"
    
    # Extract Title
    # Looks for a table row with 'Title' and captures the content
    title_match = _TITLE_RE.search(content)
    if title_match:
        info['title'] = title_match.group(1).strip()
    else:
        # Fallback: try to find it in the header
        header_match = _HEADER_TITLE_RE.search(content)
        info['title'] = header_match.group(1).strip() if header_match else "Unknown"

    # Extract Description
    desc_match = _DESC_RE.search(content)
    info['desc'] = desc_match.group(1).strip() if desc_match else ""

    return info

def get_dialogues(content: str, title: str, desc: str) -> Dict[str, str]:
    """
    Extracts dialogues if they exist in the content, otherwise returns placeholders.
    This preserves existing work if the script is re-run.
    """
    dialogues = {
        "Intro": "Dialogue Intro",
        "Teach": "Dialogue Teach",
        "Desc": "Dialogue Desc",
        "Action": "Dialogue Action"
    }

    # Helper to clean extracted dialogue
    def clean(text: str) -> str:
        # Remove quotes if present
        return text.strip().strip('"').strip("'")

    # Try to find existing dialogues in the text
    # Pattern: Remi says "{TEXT}" (In a speech bubble)
    # Note: This is a best-effort extraction based on the template structure.
    
    # Intro
    intro_match = _INTRO_RE.search(content)
    if intro_match:
        dialogues["Intro"] = clean(intro_match.group(1))

    # Teach
    teach_match = _TEACH_RE.search(content)
    if teach_match:
        dialogues["Teach"] = clean(teach_match.group(1))

    # Desc
    detail_match = _DETAIL_RE.search(content)
    if detail_match:
        dialogues["Desc"] = clean(detail_match.group(1))

    # Action
    action_match = _ACTION_RE.search(content)
    if action_match:
        dialogues["Action"] = clean(action_match.group(1))

    return dialogues

def get_safe_filename(text: str) -> str:
    """
    Returns a safe filename from the given text.
    Replaces unsafe characters with underscores.
    """
    # Remove characters that are unsafe for filenames
    safe_text = _SAFE_FILENAME_RE.sub("", text)
    # Replace spaces with underscores
    safe_text = safe_text.replace(" ", "_").strip()
    return safe_text if safe_text else "manga_file"
