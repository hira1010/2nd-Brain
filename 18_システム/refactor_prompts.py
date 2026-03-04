"""
Prompt refactoring wrapper.
Delegates to smart_refactor.py for batch processing.
"""

from _smart_refactor_runner import run_smart_refactor_all


SEPARATOR = "=" * 70


def main() -> int:
    print(SEPARATOR)
    print("Bulk Manga Prompt Refactor (Core Logic: smart_refactor.py)")
    print(SEPARATOR)

    run_smart_refactor_all()

    print("\n" + SEPARATOR)
    print("Done")
    print(SEPARATOR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
