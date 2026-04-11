# 21_ComfyUI

ComfyUI API（ポート `8188`）に接続して、画像生成ワークフローをプログラムから操作するためのフォルダです。

## 📁 構成

| ファイル | 役割 |
| :--- | :--- |
| `comfyui_controller.py` | ComfyUI API コントローラー（メインスクリプト） |
| `README.md` | このファイル |

## 🚀 使い方

### 前提条件

ComfyUI がローカルで起動していること（デフォルト: `http://127.0.0.1:8188`）

```powershell
# 依存パッケージのインストール（初回のみ）
pip install requests websocket-client
```

### 起動確認

```powershell
python 21_ComfyUI/comfyui_controller.py --status
```

出力例：
```
ComfyUI (http://127.0.0.1:8188): 🟢 起動中
```

### システム統計（VRAM など）

```powershell
python 21_ComfyUI/comfyui_controller.py --stats
```

### キュー状態確認

```powershell
python 21_ComfyUI/comfyui_controller.py --queue
```

### ワークフロー実行（JSON ファイルから）

ComfyUI の「Export (API)」で保存したワークフロー JSON を指定します。

```powershell
python 21_ComfyUI/comfyui_controller.py --run my_workflow.json
```

実行すると生成完了まで待機し、出力画像のファイル名を表示します。

### WebSocket でリアルタイム進捗表示

```powershell
python 21_ComfyUI/comfyui_controller.py --watch
```

### 生成履歴の確認

```powershell
# 全履歴
python 21_ComfyUI/comfyui_controller.py --history

# 特定のジョブ
python 21_ComfyUI/comfyui_controller.py --history <PROMPT_ID>
```

## 🐍 Python から直接呼び出す

```python
from comfyui_controller import queue_prompt, wait_for_completion, get_output_images
import json

# ワークフロー読み込み
with open("my_workflow.json", encoding="utf-8") as f:
    workflow = json.load(f)

# 実行
prompt_id = queue_prompt(workflow)
result = wait_for_completion(prompt_id)
images = get_output_images(result)
print("出力画像:", images)
```

## ⚙️ 接続設定の変更

接続先ホスト・ポートは `lib/config.py` で管理しています。

| 設定キー | デフォルト値 | 説明 |
| :--- | :--- | :--- |
| `COMFYUI_HOST` | `127.0.0.1` | ComfyUI のホスト |
| `COMFYUI_PORT` | `8188` | ComfyUI のポート |

## 🔗 関連

- `20_AI生成/` - Stability Matrix コントローラー
- `lib/config.py` - 共通設定ファイル
