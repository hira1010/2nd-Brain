import urllib.request
import urllib.error
import json

def call_tool(url, session_id, tool_name, params=None):
    try:
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params or {}
            }
        }).encode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Mcp-Session-Id': session_id
        }
        req = urllib.request.Request(url, data=data, headers=headers)
        res = urllib.request.urlopen(req)
        body = res.read().decode('utf-8')
        print(f"\n--- Output of {tool_name} ---")
        print(body)
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        print(f"Body: {e.read().decode('utf-8')[:500]}")

def init_session(url):
    data = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    headers = dict(res.getheaders())
    return headers.get('Mcp-Session-Id')

url = "http://127.0.0.1:8000/mcp"
session_id = init_session(url)
if session_id:
    call_tool(url, session_id, "list_toolsets")
