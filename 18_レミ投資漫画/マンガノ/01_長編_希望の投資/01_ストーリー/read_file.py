"""
ストーリーファイル読み取りスクリプト
エンコーディングを自動判定（cp932 → utf-8）して内容を表示する
"""

import sys

# 標準出力をUTF-8に設定（エージェント等からの読み取り対応）
sys.stdout.reconfigure(encoding="utf-8")

# エンコーディングの優先順位（Shift-JIS → UTF-8）
ENCODINGS = ["cp932", "utf-8"]

# デフォルトのファイルパス（引数がなければこれを使用）
DEFAULT_FILE = "EP16_落差の現実_P76-80.md"


def read_file(path: str) -> str:
    """
    指定パスのファイルを読み取る。
    cp932 → utf-8 の順にエンコーディングを試行する。
    """
    for enc in ENCODINGS:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise RuntimeError(f"対応するエンコーディングが見つかりません: {path}")


def main():
    """メイン処理"""
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

    try:
        content = read_file(file_path)
        print(content)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
