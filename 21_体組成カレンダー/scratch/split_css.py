import os

CSS_PATH = "public/styles.css"
OUT_DIR = "public/css"

os.makedirs(OUT_DIR, exist_ok=True)

with open(CSS_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

def write_chunk(name, start, end):
    with open(os.path.join(OUT_DIR, f"{name}.css"), "w", encoding="utf-8") as f:
        f.writelines(lines[start:end])

write_chunk("base", 0, 157)
write_chunk("layout", 157, 297)
write_chunk("components", 297, 530)
write_chunk("weekly_review", 530, 734)
write_chunk("goals", 734, 825)
write_chunk("chart", 825, 892)
write_chunk("history", 892, 986)
write_chunk("media_queries", 986, 1069)
write_chunk("calendar", 1069, 1179)
write_chunk("additive", 1179, len(lines))

print("CSS split completed successfully!")
