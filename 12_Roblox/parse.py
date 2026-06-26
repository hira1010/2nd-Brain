import json

with open(r'C:\Users\hirak\.gemini\antigravity-ide\brain\0ba02f11-a241-4879-9349-dbb25296792e\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in reversed(lines):
    data = json.loads(line)
    if data.get('type') == 'USER_INPUT':
        content = data.get('content', '')
        with open(r'c:\Users\hirak\Desktop\2nd-Brain\16_Roblox\roblox_knowledge.txt', 'w', encoding='utf-8') as out:
            out.write(content)
        break
