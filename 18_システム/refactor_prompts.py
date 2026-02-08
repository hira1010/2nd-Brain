"""
プロンプト・リファクタリング・ラッパー
smart_refactor.py の機能を利用して、全ファイルのプロンプトを一括更新します。
"""

import subprocess
import sys
import os

def main():
    print("="*70)
    print("全漫画プロンプト・リニューアル (Core Logic: smart_refactor.py)")
    print("="*70)
    
    # 18_システム ディレクトリをPythonパスに追加
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        import smart_refactor
    except ImportError:
        print("Error: smart_refactor.py not found in the same directory.")
        return

    # 全ファイルを処理
    subprocess.run([sys.executable, "smart_refactor.py", "--all"], check=True)
    
    print("\n" + "="*70)
    print("完了しました。")
    print("="*70)

if __name__ == "__main__":
    main()
