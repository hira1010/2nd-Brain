"""
Legacy wrapper for running smart_refactor.py on all target files.
"""

import os
import subprocess
import sys


def run_smart_refactor_all() -> None:
    script_path = os.path.join(os.path.dirname(__file__), "smart_refactor.py")
    subprocess.run([sys.executable, script_path, "--all"], check=True)


def main() -> None:
    print("!!! WARNING: This script is now a wrapper for smart_refactor.py !!!")
    run_smart_refactor_all()


if __name__ == "__main__":
    main()
