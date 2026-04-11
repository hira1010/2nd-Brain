import json, os
d = 'c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作/data'
for f in os.listdir(d):
  if f.endswith('.json'):
    try:
      with open(os.path.join(d,f), 'r', encoding='utf-8') as file:
        content = file.read()
        if '"name":"0"' in content or '"name": "0"' in content:
          print(f'FOUND 0 IN: {f}')
    except: pass
