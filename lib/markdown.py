import re
from typing import List, Optional, Tuple

class MarkdownEditor:
    """Markdownファイルの編集を抽象化するクラス。"""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.splitlines()

    def insert_after_marker(self, marker: str, entry: str) -> bool:
        """マーカー（見出し等）の直後にテキストを挿入します。"""
        if marker in self.content:
            self.content = self.content.replace(marker, f"{marker}\n\n{entry}\n")
            self.lines = self.content.splitlines()
            return True
        return False

    def update_table_cell(self, header_keywords: List[str], row_match_func, col_index: int, value: str, bold: bool = True) -> bool:
        """Markdownテーブルの特定のセルを更新します。"""
        # 実装の詳細は sync_assets 等の移行時に洗練させる
        pass

    def update_mermaid_array(self, key: str, value: str) -> bool:
        """Mermaidチャートの配列 [a, b, c] に要素を追加します。"""
        pattern = rf"{re.escape(key)} \[(.*?)\]"
        match = re.search(pattern, self.content)
        if match:
            current = match.group(1)
            # 重複チェック
            if value in current:
                return False
            new_array = f"{key} [{current}, {value}]" if current else f"{key} [{value}]"
            self.content = self.content.replace(match.group(0), new_array)
            self.lines = self.content.splitlines()
            return True
        return False

    def get_content(self) -> str:
        return self.content
