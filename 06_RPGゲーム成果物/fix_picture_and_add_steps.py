import json
import os

base_dir = r"c:\Users\hirak\Desktop\2nd-Brain\06_RPGゲーム成果物\data"

# Ensure Map001 Victory Event conditions are perfectly valid
with open(os.path.join(base_dir, "Map001.json"), "r", encoding="utf-8") as f:
    map1 = json.load(f)

perfect_conditions = {
    "actorId": 1, "actorValid": False,
    "enemyIndex": 0, "enemyValid": False, 
    "itemId": 1, "itemValid": False,
    "selfSwitchCh": "A", "selfSwitchValid": False,
    "switch1Id": 1, "switch1Valid": False,
    "switch2Id": 1, "switch2Valid": False,
    "variableId": 1, "variableValid": False, "variableValue": 0
}
perfect_conditions_B = dict(perfect_conditions)
perfect_conditions_B["selfSwitchCh"] = "B"
perfect_conditions_B["selfSwitchValid"] = True

for ev in map1["events"]:
    if ev and ev.get("name") == "勝利画面":
        ev["pages"][0]["conditions"] = perfect_conditions
        ev["pages"][1]["conditions"] = perfect_conditions_B

with open(os.path.join(base_dir, "Map001.json"), "w", encoding="utf-8") as f:
    json.dump(map1, f, separators=(',', ':'), ensure_ascii=False)


# Add parallel process for 3 steps "ムラムラ" dialogue in Map002
with open(os.path.join(base_dir, "Map002.json"), "r", encoding="utf-8") as f:
    map2 = json.load(f)

new_event_id = 1
while new_event_id < len(map2["events"]) and map2["events"][new_event_id] is not None:
    if map2["events"][new_event_id].get("name") == "ムラムラチェッカー":
        break
    new_event_id += 1

if new_event_id >= len(map2["events"]):
    map2["events"].append(None)

script_lines = [
    "let s = $gameParty.steps();",
    "let last = $gameVariables.value(1);",
    "if (last === 0) { $gameVariables.setValue(1, s); }",
    "else if (s >= last + 3) {",
    "  $gameVariables.setValue(1, s);",
    "  $gameMessage.setFaceImage('', 0);",
    "  $gameMessage.setBackground(0);",
    "  $gameMessage.setPositionType(2);",
    "  $gameMessage.add('ムラムラしてきた');",
    "}"
]

mura_event = {
    "id": new_event_id,
    "name": "ムラムラチェッカー",
    "note": "",
    "x": 0, "y": 0,
    "pages": [
        {
            "conditions": perfect_conditions,
            "directionFix": False,
            "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
            "list": [
                {"code": 355, "indent": 0, "parameters": [script_lines[0]]}
            ] + [{"code": 655, "indent": 0, "parameters": [line]} for line in script_lines[1:]] + [
                {"code": 230, "indent": 0, "parameters": [10]}, # wait 10 frames to not lag
                {"code": 0, "indent": 0, "parameters": []}
            ],
            "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": 0, "priorityType": 0, "stepAnime": False, "through": True, "trigger": 4, "walkAnime": False # Trigger 4 = Parallel
        }
    ]
}

map2["events"][new_event_id] = mura_event

with open(os.path.join(base_dir, "Map002.json"), "w", encoding="utf-8") as f:
    json.dump(map2, f, separators=(',', ':'), ensure_ascii=False)


# Update original project too
try:
    with open(os.path.join(base_dir, "Map001.json"), "r", encoding="utf-8") as src:
        with open(r"c:\Users\hirak\Desktop\2nd-Brain\25_RPGツクールフォルダ\data\Map001.json", "w", encoding="utf-8") as dst: dst.write(src.read())
    with open(os.path.join(base_dir, "Map002.json"), "r", encoding="utf-8") as src:
        with open(r"c:\Users\hirak\Desktop\2nd-Brain\25_RPGツクールフォルダ\data\Map002.json", "w", encoding="utf-8") as dst: dst.write(src.read())
except Exception:
    pass

print("Map001 Victory Event Fixed. Map002 Mura-mura Parallel Event Added.")
