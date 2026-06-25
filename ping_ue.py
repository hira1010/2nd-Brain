import urllib.request
import urllib.error
import sys

def ping(url):
    print(f"\n--- Pinging {url} ---")
    try:
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
        print(f"Status: {res.status} {res.reason}")
        print("Headers:")
        for k, v in res.getheaders():
            print(f"  {k}: {v}")
        body = res.read().decode('utf-8', errors='ignore')
        print(f"Body: {body[:500]}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        try:
            print(f"Body: {e.read().decode('utf-8')[:500]}")
        except:
            pass
    except Exception as e:
        print(f"Error: {e}")
        
ping("http://127.0.0.1:8000/mcp")
ping("http://127.0.0.1:8000/sse")
ping("http://127.0.0.1:8000/")
