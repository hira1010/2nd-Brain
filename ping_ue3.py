import urllib.request
import urllib.error
import json

def test_post(url, method, params=None):
    print(f"\n--- Testing POST {url} method: {method} ---")
    try:
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }).encode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Mcp-Session-Id': '1234'
        }
        req = urllib.request.Request(url, data=data, headers=headers)
        res = urllib.request.urlopen(req)
        print(f"Status: {res.status} {res.reason}")
        body = res.read().decode('utf-8')
        print(f"Body: {body}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        try:
            print(f"Body: {e.read().decode('utf-8')[:500]}")
        except:
            pass

test_post("http://127.0.0.1:8000/mcp", "initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "test", "version": "1.0"}
})
test_post("http://127.0.0.1:8000/mcp", "tools/list")
