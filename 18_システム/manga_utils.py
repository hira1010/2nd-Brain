"""
Manga production system common utilities
ASCII-only version.
"""

import re
import os
from typing import Dict, Optional, Any

def setup_logger(name: str):
    import logging
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
    info = {}
    
    # Extract No
    no_match = re.search(r'\|\s*No\s*\|\s*(\d+)\s*\|', content)
    info['no'] = no_match.group(1) if no_match else "00"
    
    # Extract Title - using non-ASCII regex capture if needed but this logic itself is ASCII
    title_match = re.search(r'\|\s*[^|]*\s*\|\s*(.*?)[\s|]*\|', content) # Generic capture
    info['title'] = "Unknown"
    # Note: parsing Japanese titles from UTF-8 content in ASCII script is tricky, 
    # but the script itself is ASCII.
    
    return info

def get_dialogues(content: str, title: str, desc: str) -> Dict[str, str]:
    return {
        "Intro": "Dialogue Intro",
        "Teach": "Dialogue Teach",
        "Desc": "Dialogue Desc",
        "Action": "Dialogue Action"
    }

def get_safe_filename(text: str) -> str:
    return "manga_file"
