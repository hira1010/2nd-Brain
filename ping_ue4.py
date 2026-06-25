import urllib.request
import urllib.error
import json

def test_post(url, method, params=None, headers=None):
    print(f"\n--- Testing POST {url} method: {method} ---")
    try:
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }).encode('utf-8')
        req_headers = {'Content-Type': 'application/json'}
        if headers:
            req_headers.update(headers)
            
        req = urllib.request.Request(url, data=data, headers=req_headers)
        res = urllib.request.urlopen(req)
        print(f"Status: {res.status} {res.reason}")
        print("Headers:")
        for k, v in res.getheaders():
            print(f"  {k}: {v}")
        body = res.read().decode('utf-8')
        print(f"Body: {body}")
        return dict(res.getheaders())
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        try:
            print(f"Body: {e.read().decode('utf-8')[:500]}")
        except:
            pass
        return {}

res_headers = test_post("http://127.0.0.1:8000/mcp", "initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "test", "version": "1.0"}
})

session_id = res_headers.get('Mcp-Session-Id')
if session_id:
    test_post("http://127.0.0.1:8000/mcp", "tools/list", headers={'Mcp-Session-Id': session_id})
else:
    print("No session ID found in response headers.")
