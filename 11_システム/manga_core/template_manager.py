import logging
from pathlib import Path
from typing import Dict, Optional

from manga_core.file_handler import FileHandler

logger = logging.getLogger(__name__)


class TemplateManager:
    """
    Manages loading and formatting of manga templates.
    """
    
    def __init__(self, template_dir: Path):
        self.template_dir = Path(template_dir)
        self.templates: Dict[str, str] = {}

    def _resolve_template_path(self, template_name: str) -> Path:
        return self.template_dir / template_name

    def load_template(self, template_name: str) -> Optional[str]:
        """
        Loads a template string from a file.
        """
        cached = self.templates.get(template_name)
        if cached is not None:
            return cached

        template_path = self._resolve_template_path(template_name)
        content = FileHandler.read_file(template_path)
        if content is None:
            logger.error("Failed to load template %s from %s", template_name, template_path)
            return None
        self.templates[template_name] = content
        return content
