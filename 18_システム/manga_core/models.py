from dataclasses import dataclass, field
from typing import Dict, Optional, List

@dataclass
class MangaEpisode:
    """
    Represents a manga episode prompt file.
    """
    no: str = "00"
    title: str = "Unknown"
    desc: str = ""
    category: str = "Uncategorized"
    dialogues: Dict[str, str] = field(default_factory=dict)
    
    # Optional fields for future use like tags, scene settings etc.
    tags: List[str] = field(default_factory=list)

@dataclass
class VisualLock:
    """
    Represents visual settings for a character.
    """
    name: str
    desc: str
