"""
Legacy wrapper for running smart_refactor.py on all target files.
"""

from _smart_refactor_runner import run_smart_refactor_all


def main() -> int:
    print("!!! WARNING: This script is now a wrapper for smart_refactor.py !!!")
    run_smart_refactor_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
