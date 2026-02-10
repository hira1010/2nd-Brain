"""
Prompt refactoring wrapper.
Delegates to smart_refactor.py for batch processing.
"""

import os
import subprocess
import sys


def run_smart_refactor_all() -> None:
    script_path = os.path.join(os.path.dirname(__file__), "smart_refactor.py")
    subprocess.run([sys.executable, script_path, "--all"], check=True)


def main() -> None:
    print("=" * 70)
    print("Bulk Manga Prompt Refactor (Core Logic: smart_refactor.py)")
    print("=" * 70)

    run_smart_refactor_all()

    print("\n" + "=" * 70)
    print("Done")
    print("=" * 70)


if __name__ == "__main__":
    main()
