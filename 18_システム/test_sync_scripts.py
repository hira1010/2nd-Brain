import importlib.util
import unittest
from pathlib import Path


def load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE_DIR = Path(__file__).resolve().parent
SYNC_WEIGHT = load_module("sync_weight_module", BASE_DIR / "sync_weight.py")
SYNC_ASSETS = load_module("sync_assets_module", BASE_DIR / "sync_assets.py")


class TestSyncWeight(unittest.TestCase):
    def test_normalize_date(self):
        self.assertEqual(SYNC_WEIGHT.normalize_date("02/07"), "2/7")
        self.assertEqual(SYNC_WEIGHT.normalize_date("2/17"), "2/17")

    def test_entry_exists(self):
        content = "### 2/17 (月) ── 92.8kg\n"
        self.assertTrue(SYNC_WEIGHT.entry_exists(content, "2/17"))
        self.assertTrue(SYNC_WEIGHT.entry_exists(content, "02/17"))
        self.assertFalse(SYNC_WEIGHT.entry_exists(content, "2/16"))

    def test_update_mermaid_chart_append_once(self):
        content = (
            "```mermaid\n"
            "xychart-beta\n"
            "x-axis [2/16]\n"
            "line [93.6]\n"
            "```\n"
        )
        updated = SYNC_WEIGHT.update_mermaid_chart(content, "2/17", "92.8")
        self.assertIn("x-axis [2/16, 2/17]", updated)
        self.assertIn("line [93.6, 92.8]", updated)

        updated_again = SYNC_WEIGHT.update_mermaid_chart(updated, "2/17", "92.8")
        self.assertEqual(updated, updated_again)


class TestSyncAssets(unittest.TestCase):
    def test_update_markdown_table(self):
        table = (
            "| 年 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |\n"
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n"
            "| 1月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 2月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 3月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 4月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 5月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 6月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 7月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 8月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 9月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 10月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 11月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| 12月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |\n"
            "| **合計** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |\n"
            "| **増加率** | - | - | - | - | - | - | - | - | - | - |\n"
            "| **資産** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** |\n"
        )

        snapshot = SYNC_ASSETS.AssetSnapshot(
            months={m: str(100 + m) for m in range(1, 13)},
            total="44306",
            growth_rate="9%",
            asset="2200万",
        )
        updated = SYNC_ASSETS.update_markdown_table(table, snapshot)

        self.assertIn("| 1月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **101** |", updated)
        self.assertIn("| 12月 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **112** |", updated)
        self.assertIn("| **合計** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **44306** |", updated)
        self.assertIn("| **増加率** | - | - | - | - | - | - | - | - | - | 9% |", updated)
        self.assertIn("| **資産** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **0万** | **2200万** |", updated)


if __name__ == "__main__":
    unittest.main()
