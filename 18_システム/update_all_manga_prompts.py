"""
Legacy wrapper for running smart_refactor.py on all target files.
"""

from _smart_refactor_runner import run_smart_refactor_all


def main() -> None:
    print("!!! WARNING: This script is now a wrapper for smart_refactor.py !!!")
    run_smart_refactor_all()


if __name__ == "__main__":
    main()
