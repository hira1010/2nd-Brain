import os

SCRIPT_PATH = "public/script.js"
OUT_DIR = "public/js"

os.makedirs(OUT_DIR, exist_ok=True)

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

def write_chunk(name, start, end):
    with open(os.path.join(OUT_DIR, f"{name}.js"), "w", encoding="utf-8") as f:
        f.writelines(lines[start:end])

write_chunk("config", 0, 54)
write_chunk("state", 54, 105)
write_chunk("main", 105, 159)
write_chunk("parser", 159, 428)
write_chunk("ui", 428, 1161)
write_chunk("chart", 1161, 1343)
write_chunk("history", 1343, 1369)
write_chunk("calendar", 1369, 1521)
write_chunk("ui_actions", 1521, 1570)
write_chunk("api_storage", 1570, 1835)
write_chunk("utils", 1835, 1956)
write_chunk("additive", 1956, 2015)

print("Split completed successfully!")
