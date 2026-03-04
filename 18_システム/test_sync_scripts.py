import importlib.util
import unittest
from pathlib import Path
import os
import sys

# プロジェクトルートをパスに追加
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))

def load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module

SYNC_WEIGHT = load_module("sync_weight_module", BASE_DIR / "sync_weight.py")
SYNC_ASSETS = load_module("sync_assets_module", BASE_DIR / "sync_assets.py")

class TestSyncWeight(unittest.TestCase):
    def test_normalize_date(self):
        self.assertEqual(SYNC_WEIGHT.normalize_date("02/07"), "2/7")
        self.assertEqual(SYNC_WEIGHT.normalize_date("2/17"), "2/17")

class TestSyncAssets(unittest.TestCase):
    def test_format_val(self):
        self.assertEqual(SYNC_ASSETS.format_val(100), "100")
        self.assertEqual(SYNC_ASSETS.format_val("0%"), "-")
        self.assertEqual(SYNC_ASSETS.format_val("9.5", is_percent=True), "9%")

if __name__ == "__main__":
    unittest.main()
