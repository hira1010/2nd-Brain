"""ComfyUI API Controller - ComfyUI（ポート8188）との接続・制御スクリプト。"""

import json
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import websocket  # websocket-client

# プロジェクトルートをパスに追加
_current = Path(__file__).resolve().parent
_project_root = _current.parent
if str(_project_root) not in sys.path:
    sys.path.append(str(_project_root))

from lib import config

# ----- 接続設定 -----
COMFYUI_HOST: str = config.COMFYUI_HOST
COMFYUI_PORT: int = config.COMFYUI_PORT
BASE_URL: str = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"
WS_URL: str = f"ws://{COMFYUI_HOST}:{COMFYUI_PORT}/ws"


# ====================================================================
# ユーティリティ
# ====================================================================

def _get(endpoint: str, timeout: int = 10) -> Any:
    """GETリクエストを送信してJSONを返す。"""
    response = requests.get(f"{BASE_URL}{endpoint}", timeout=timeout)
    response.raise_for_status()
    return response.json()


def _post(endpoint: str, data: Dict[str, Any], timeout: int = 30) -> Any:
    """POSTリクエストを送信してJSONを返す。"""
    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=data,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


# ====================================================================
# 状態確認
# ====================================================================

def is_running() -> bool:
    """ComfyUIが起動中かどうかを確認する。"""
    try:
        _get("/system_stats", timeout=3)
        return True
    except Exception:
        return False


def get_system_stats() -> Dict[str, Any]:
    """システム統計情報（GPU VRAM など）を取得する。"""
    return _get("/system_stats")


def get_queue() -> Dict[str, Any]:
    """現在のキュー状態（実行中・待機中）を取得する。"""
    return _get("/queue")


def get_history(prompt_id: Optional[str] = None) -> Dict[str, Any]:
    """生成履歴を取得する。prompt_id を指定すると特定のジョブのみ返す。"""
    endpoint = f"/history/{prompt_id}" if prompt_id else "/history"
    return _get(endpoint)


# ====================================================================
# プロンプト実行
# ====================================================================

def queue_prompt(workflow: Dict[str, Any], client_id: Optional[str] = None) -> str:
    """
    ワークフロー（workflow API形式）をキューに追加して prompt_id を返す。

    Args:
        workflow: ComfyUI のワークフロー（API形式のJSON辞書）
        client_id: WebSocket クライアントID（省略時は自動生成）

    Returns:
        prompt_id（str）
    """
    if client_id is None:
        client_id = str(uuid.uuid4())

    payload = {"prompt": workflow, "client_id": client_id}
    result = _post("/prompt", payload)
    prompt_id: str = result["prompt_id"]
    print(f"✅ キューに追加しました: prompt_id={prompt_id}")
    return prompt_id


def wait_for_completion(prompt_id: str, timeout: int = 300) -> Dict[str, Any]:
    """
    prompt_id の生成が完了するまでポーリングして待機する。

    Args:
        prompt_id: queue_prompt() が返したID
        timeout: タイムアウト秒数（デフォルト300秒）

    Returns:
        完了した履歴データ
    """
    print(f"⏳ 生成完了を待機中 (prompt_id={prompt_id}) ...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        history = get_history(prompt_id)
        if prompt_id in history:
            print("✅ 生成完了！")
            return history[prompt_id]
        time.sleep(2)
    raise TimeoutError(f"タイムアウト: prompt_id={prompt_id} が {timeout}秒 以内に完了しませんでした。")


def get_output_images(history_entry: Dict[str, Any]) -> list[str]:
    """
    履歴エントリから出力画像のファイル名一覧を取得する。

    Args:
        history_entry: wait_for_completion() が返した履歴データ

    Returns:
        画像ファイル名のリスト
    """
    images = []
    outputs = history_entry.get("outputs", {})
    for node_output in outputs.values():
        for image in node_output.get("images", []):
            images.append(image["filename"])
    return images


def download_image(filename: str, subfolder: str = "", image_type: str = "output") -> bytes:
    """
    ComfyUI から画像データをダウンロードして bytes を返す。

    Args:
        filename: 画像ファイル名
        subfolder: サブフォルダ名（省略可）
        image_type: "output" or "input" or "temp"

    Returns:
        画像のバイトデータ
    """
    params = {"filename": filename, "subfolder": subfolder, "type": image_type}
    response = requests.get(f"{BASE_URL}/view", params=params, timeout=30)
    response.raise_for_status()
    return response.content


def upload_image(image_path: Path, overwrite: bool = False) -> Dict[str, Any]:
    """
    画像を ComfyUI にアップロードする。

    Args:
        image_path: アップロードする画像のパス
        overwrite: すでに存在する場合に上書きするかどうか

    Returns:
        ComfyUI からのレスポンス（ファイル名などを含む）
    """
    files = {"image": open(image_path, "rb")}
    data = {"overwrite": str(overwrite).lower()}
    response = requests.post(f"{BASE_URL}/upload/image", files=files, data=data, timeout=30)
    response.raise_for_status()
    return response.json()


# ====================================================================
# WebSocket リアルタイム監視
# ====================================================================

def watch_progress(client_id: Optional[str] = None) -> None:
    """
    WebSocket で ComfyUI の進捗をリアルタイム表示する（Ctrl+C で終了）。

    Args:
        client_id: WebSocket クライアントID（省略時は自動生成）
    """
    if client_id is None:
        client_id = str(uuid.uuid4())

    ws_url_with_id = f"{WS_URL}?clientId={client_id}"
    print(f"🔌 WebSocket 接続中: {ws_url_with_id}")

    def on_message(ws, message):  # type: ignore
        try:
            data = json.loads(message)
            msg_type = data.get("type", "")
            if msg_type == "progress":
                value = data["data"]["value"]
                maximum = data["data"]["max"]
                print(f"\r📊 進捗: {value}/{maximum}", end="", flush=True)
            elif msg_type == "executed":
                print(f"\n✅ ノード実行完了: {data['data'].get('node', '')}")
            elif msg_type == "execution_complete":
                print("\n🎉 生成完了！")
        except json.JSONDecodeError:
            pass  # バイナリ（画像プレビュー）は無視

    def on_error(ws, error):  # type: ignore
        print(f"\n❌ WebSocket エラー: {error}")

    def on_close(ws, close_status_code, close_msg):  # type: ignore
        print("\n🔌 WebSocket 切断")

    ws = websocket.WebSocketApp(
        ws_url_with_id,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


# ====================================================================
# CLI エントリーポイント
# ====================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ComfyUI Controller")
    parser.add_argument("--status", action="store_true", help="ComfyUI の起動確認")
    parser.add_argument("--stats", action="store_true", help="システム統計を表示")
    parser.add_argument("--queue", action="store_true", help="キュー状態を表示")
    parser.add_argument("--history", metavar="PROMPT_ID", nargs="?", const="",
                        help="生成履歴を表示（IDなしで全件）")
    parser.add_argument("--watch", action="store_true", help="WebSocket で進捗をリアルタイム表示")
    parser.add_argument("--run", metavar="WORKFLOW_JSON",
                        help="ワークフローJSONファイルをキューに追加して完了まで待機")

    args = parser.parse_args()

    if args.status:
        status = "🟢 起動中" if is_running() else "🔴 停止中"
        print(f"ComfyUI ({BASE_URL}): {status}")

    elif args.stats:
        stats = get_system_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))

    elif args.queue:
        q = get_queue()
        running = q.get("queue_running", [])
        pending = q.get("queue_pending", [])
        print(f"🔄 実行中: {len(running)} 件 / 待機中: {len(pending)} 件")
        if running:
            print("  実行中:", running)
        if pending:
            print("  待機中:", pending)

    elif args.history is not None:
        pid = args.history if args.history else None
        history = get_history(pid)
        print(json.dumps(history, indent=2, ensure_ascii=False))

    elif args.watch:
        watch_progress()

    elif args.run:
        workflow_path = Path(args.run)
        if not workflow_path.exists():
            print(f"❌ ファイルが見つかりません: {workflow_path}")
            sys.exit(1)
        with open(workflow_path, encoding="utf-8") as f:
            workflow = json.load(f)
        prompt_id = queue_prompt(workflow)
        result = wait_for_completion(prompt_id)
        images = get_output_images(result)
        print(f"📁 出力画像: {images}")

    else:
        parser.print_help()
