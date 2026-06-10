import subprocess
import json
import time

def send_rpc(proc, method, params=None, id=1):
    msg = {
        "jsonrpc": "2.0",
        "method": method,
        "id": id
    }
    if params is not None:
        msg["params"] = params
    
    # MCP requires JSON separated by newlines usually, or proper Content-Length headers?
    # Wait, Claude's MCP stdio uses just \n delimited JSON.
    req = json.dumps(msg) + "\n"
    proc.stdin.write(req)
    proc.stdin.flush()
    
    # Read response
    out = proc.stdout.readline()
    return out

proc = subprocess.Popen(
    ["C:\\Users\\hirak\\AppData\\Local\\Roblox\\Versions\\version-8ec813a8524f409b\\StudioMCP.exe"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print(send_rpc(proc, "tools/list", id=1))
proc.terminate()
