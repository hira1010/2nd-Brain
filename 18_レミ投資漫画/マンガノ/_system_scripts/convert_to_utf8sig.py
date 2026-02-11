import os
import codecs

_TARGET_FILES = [
    "generate_mangano.py",
    "manga_config.py",
    "manga_utils.py",
    "fix_manga_prompts.py",
]


def _read_text(path: str) -> str:
    try:
        with codecs.open(path, "r", "utf-8-sig") as f:
            return f.read()
    except UnicodeDecodeError:
        with codecs.open(path, "r", "utf-8") as f:
            return f.read()


def convert_files() -> None:
    base_dir = os.getcwd()

    for filename in _TARGET_FILES:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            continue

        try:
            content = _read_text(filepath)
            with codecs.open(filepath, "w", "utf-8-sig") as f:
                f.write(content)
            print(f"Converted {filename} to UTF-8 with BOM")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")


if __name__ == "__main__":
    convert_files()
