import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class TemplateManager:
    """
    Manages loading and formatting of manga templates.
    """
    
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.templates = {}

    def load_template(self, template_name: str) -> Optional[str]:
        """
        Loads a template string from a file.
        """
        if template_name in self.templates:
            return self.templates[template_name]
            
        template_path = self.template_dir / template_name
        try:
            content = template_path.read_text(encoding="utf-8")
            self.templates[template_name] = content
            return content
        except Exception as e:
            logger.error(f"Failed to load template {template_name} from {template_path}: {e}")
            return None
