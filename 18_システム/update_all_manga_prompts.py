"""
全漫画プロンプト一括更新 (LEGACY WRAPPER)
このスクリプトは非推奨です。同様の機能は smart_refactor.py --all で実行可能です。
"""

import subprocess
import sys
import os

def main():
    print("!!! WARNING: This script is now a wrapper for smart_refactor.py !!!")
    
    # smart_refactor.py を実行
    script_path = os.path.join(os.path.dirname(__file__), "smart_refactor.py")
    subprocess.run([sys.executable, script_path, "--all"], check=True)

if __name__ == "__main__":
    main()
