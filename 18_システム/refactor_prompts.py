"""
Prompt refactoring wrapper.
Delegates to smart_refactor.py for batch processing.
"""

from _smart_refactor_runner import run_smart_refactor_all


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
