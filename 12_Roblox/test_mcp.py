import subprocess
import json
import time
import concurrent.futures

class MCPClient:
    """専用の受付係（Roblox Studioとのやり取りを担当）"""
    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.process = None

    def __enter__(self):
        """自動ドアを開ける処理（開始時）"""
        self.process = subprocess.Popen(
            [self.executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """自動ドアを閉める処理（終了時、またはエラー時）"""
        if self.process:
            self.process.terminate()

    def send_rpc(self, method, params=None, rpc_id=1, timeout_sec=5):
        """注文を渡して返事をもらう処理（待ち時間のルール付き）"""
        if not self.process:
            raise RuntimeError("お店（プロセス）が開いていません。")
            
        msg = {
            "jsonrpc": "2.0",
            "method": method,
            "id": rpc_id
        }
        if params is not None:
            msg["params"] = params
        
        # 注文を投函
        req = json.dumps(msg) + "\n"
        self.process.stdin.write(req)
        self.process.stdin.flush()
        
        # 返事を待つ（タイマーをセット）
        def _wait_for_reply():
            return self.process.stdout.readline()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(_wait_for_reply)
            try:
                # 指定した時間だけ待つ
                out = future.result(timeout=timeout_sec)
                return out
            except concurrent.futures.TimeoutError:
                return f"【お知らせ】{timeout_sec}秒待ちましたが、お返事が来ませんでした。"

if __name__ == "__main__":
    MCP_EXE = r"C:\Users\hirak\AppData\Local\Roblox\Versions\version-3da9d00a092c4d59\StudioMCP.exe"
    
    # with文が「自動ドア」の仕組み。ブロックが終わると自動で__exit__が呼ばれ安全に閉じます。
    with MCPClient(MCP_EXE) as client:
        print("お店を開きました。注文（tools/list）を送ります...")
        response = client.send_rpc("tools/list", rpc_id=1)
        print("お返事を受け取りました：\n" + response)
    print("お店を安全に閉めました。")
