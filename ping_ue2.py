import urllib.request
import urllib.error
import json

def test_sse(url):
    print(f"\n--- Testing SSE GET {url} ---")
    try:
        req = urllib.request.Request(url, headers={'Accept': 'text/event-stream'})
        res = urllib.request.urlopen(req)
        print(f"Status: {res.status} {res.reason}")
        print("Headers:")
        for k, v in res.getheaders():
            print(f"  {k}: {v}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")

def test_post(url):
    print(f"\n--- Testing POST {url} ---")
    try:
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
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

test_sse("http://127.0.0.1:8000/mcp")
test_post("http://127.0.0.1:8000/mcp")
