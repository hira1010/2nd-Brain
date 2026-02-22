"""Shared helper for invoking smart_refactor.py."""

import subprocess
import sys
from pathlib import Path


def run_smart_refactor_all() -> None:
    script_path = Path(__file__).resolve().parent / "smart_refactor.py"
    subprocess.run([sys.executable, str(script_path), "--all"], check=True)
