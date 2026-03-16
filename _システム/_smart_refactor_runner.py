"""Shared helper for invoking smart_refactor.py."""

import subprocess
import sys
from pathlib import Path
from typing import Sequence


def _script_path() -> Path:
    return Path(__file__).resolve().parent / "smart_refactor.py"


def run_smart_refactor(args: Sequence[str]) -> None:
    subprocess.run([sys.executable, str(_script_path()), *args], check=True)


def run_smart_refactor_all() -> None:
    run_smart_refactor(["--all"])
