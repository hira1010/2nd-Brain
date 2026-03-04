import importlib.util
import tempfile
import unittest
from pathlib import Path

from lib import sheets, utils


def load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE_DIR = Path(__file__).resolve().parent
SYNC_ANTIGRAVITY = load_module("sync_antigravity_module", BASE_DIR / "sync_antigravity.py")


class TestLibHelpers(unittest.TestCase):
    def test_get_safe_filename(self):
        self.assertEqual(utils.get_safe_filename('a/b:c*?"<>| d'), "abc_d")
        self.assertEqual(utils.get_safe_filename("  "), "__")

    def test_build_csv_export_url(self):
        url = sheets._build_csv_export_url("sheet-id", "123")
        self.assertEqual(
            url,
            "https://docs.google.com/spreadsheets/d/sheet-id/export?format=csv&gid=123",
        )


class TestSyncAntigravityHelpers(unittest.TestCase):
    def test_iter_existing_sync_dirs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            (base / "brain").mkdir()
            (base / "knowledge").mkdir()

            existing = SYNC_ANTIGRAVITY._iter_existing_sync_dirs(
                base,
                ("brain", "conversations", "knowledge", "global_skills"),
            )
            self.assertEqual(existing, ["brain", "knowledge"])


if __name__ == "__main__":
    unittest.main()
