import os
import time

dir_path = r"c:\Users\hirak\Desktop\2nd-Brain\24_UnrealMCP"
os.makedirs(dir_path, exist_ok=True)

readme_path = os.path.join(dir_path, "README.md")
readme_content = """# Unreal Engine AI連携（MCP）用フォルダ

このフォルダは、AI（私）がUnreal Engineを直接操作するための準備フォルダです。

## 🎮 次にあなたがUnreal Engineで行うこと

1. Unreal Engine 5.8のエディタを開きます。
2. 上部メニューの **編集** ＞ **プラグイン** を開きます。
3. 検索窓に「**Unreal MCP**」と入力し、出てきたプラグインにチェックを入れて有効化します。
4. エディタを再起動するよう求められるので、再起動します。
5. 再起動後、**編集** ＞ **エディタの環境設定** を開きます。
6. 左のメニューから **Model Context Protocol** を選び、「Auto Start Server（サーバーの自動起動）」にチェックを入れます。

これで、AIがUnreal Engineと「お話し」できるようになります！
"""

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_content)

time.sleep(3)

config_path = os.path.join(dir_path, "config.txt")
config_content = """【AI用設定ファイル】
このファイルはAIがUnreal Engineを見つけるための目印です。
"""
with open(config_path, "w", encoding="utf-8") as f:
    f.write(config_content)

time.sleep(3)
print("セットアップ完了")
