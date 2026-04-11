"""RenPy MCP configuration."""

from dataclasses import dataclass, field
from pathlib import Path
import os


@dataclass
class RenPyConfig:
    """Configuration for RenPy SDK and project paths."""

    sdk_path: Path = field(default_factory=lambda: _default_sdk_path())
    project_path: Path | None = None

    @property
    def renpy_exe(self) -> Path:
        """Path to the RenPy executable."""
        if os.name == "nt":
            return self.sdk_path / "renpy.exe"
        return self.sdk_path / "renpy.sh"

    def validate(self) -> list[str]:
        """Return list of validation errors, empty if valid."""
        errors = []
        if not self.sdk_path.exists():
            errors.append(f"SDK path does not exist: {self.sdk_path}")
        elif not self.renpy_exe.exists():
            errors.append(f"RenPy executable not found: {self.renpy_exe}")
        if self.project_path and not self.project_path.exists():
            errors.append(f"Project path does not exist: {self.project_path}")
        return errors


def _default_sdk_path() -> Path:
    env = os.environ.get("RENPY_SDK_PATH")
    if env:
        return Path(env)
    return Path(".")
