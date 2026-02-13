"""
Manga production system common utilities.
Provides logging, text extraction, and sanitization helper functions.
"""

import logging
import re
from typing import Dict, Optional

# Regex Patterns
_NO_RE = re.compile(r"\|\s*No\s*\|\s*(\d+)\s*\|")
_TITLE_RE = re.compile(r"\|\s*Title\s*\|\s*(.*?)[\s|]*\|", re.IGNORECASE)
_HEADER_TITLE_RE = re.compile(r"#\s*(?:Episode|No\.)\s*\d+\s*[:\.]?\s*(.*?)($|\s)", re.IGNORECASE)
_DESC_RE = re.compile(r"\|\s*Description\s*\|\s*(.*?)[\s|]*\|", re.IGNORECASE)

# Old Template Dialogue Patterns
_INTRO_RE = re.compile(r'(?:Remi says "|STRICT SPEECH BUBBLE.*?: \')([^\'"]+)(?:"|\')')
_TEACH_RE = re.compile(r'(?:She says "|STRICT SPEECH BUBBLE.*?: \')([^\'"]+)(?:"|\')')
# Simplified patterns - can be improved if more context needed
# But for now, capturing *any* speech bubble content might be safer if structure varies
# Let's try to match the specific keys used in typical files.

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
    # If not found in table, try header "Episode X"
    if not no_match:
        header_no_match = re.search(r"#\s*Episode\s*(\d+)", content, re.IGNORECASE)
        info['no'] = header_no_match.group(1) if header_no_match else "00"
    else:
        info['no'] = no_match.group(1)
    
    # Extract Title
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
    Extracts dialogues if they exist in the content.
    This is complex because formats vary (Old vs New).
    We use a best-effort approach.
    """
    # Default placeholders
    dialogues = {
        "Intro": "Dialogue Intro",
        "Teach": "Dialogue Teach",
        "Desc": "Dialogue Desc",
        "Action": "Dialogue Action"
    }

    # Helper to clean extracted dialogue
    def clean(text: str) -> str:
        return text.strip().strip('"').strip("'")

    # Trying to extract roughly based on position or context keywords if standard regex fails
    # Standard format usually has 'Remi says "..."' or 'STRICT SPEECH BUBBLE: "..."'
    
    # Simple extraction strategy: Find all speech bubbles content
    # This might mix them up, but better than nothing if structure is broken
    bubbles = re.findall(r"(?:STRICT SPEECH BUBBLE|says)\s*[:\.]?\s*['\"](.*?)['\"]", content)
    
    if len(bubbles) >= 4:
        # If we found enough bubbles, assume they correspond to the 4 key slots
        dialogues["Intro"] = clean(bubbles[0])
        dialogues["Teach"] = clean(bubbles[1]) # Usually 2nd bubble on page 1
        dialogues["Desc"] = clean(bubbles[2])  # Page 2 start
        dialogues["Action"] = clean(bubbles[-1]) # Last one usually Yuto
    
    return dialogues

def get_safe_filename(text: str) -> str:
    """
    Returns a safe filename from the given text.
    """
    safe_text = _SAFE_FILENAME_RE.sub("", text)
    safe_text = safe_text.replace(" ", "_").strip()
    return safe_text if safe_text else "manga_file"
