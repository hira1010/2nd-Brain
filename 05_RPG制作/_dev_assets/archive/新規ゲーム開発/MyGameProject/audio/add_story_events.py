import json, shutil

# ============================================================
# ストーリー・NPCイベント追加スクリプト
# Map001: 村人おじさん、研究者、少女、看板×2
# Map002: 迷い込んだ旅人、石碑、入場演出
# ============================================================

def make_npc_event(event_id, name, x, y, lines_page1, lines_page2=None, face_name="", face_index=0, direction=2):
    """NPCイベントを作成（2ページ: 初回/2回目以降）"""

    def build_message_list(lines, face="", fidx=0):
        result = [{"code": 101, "indent": 0, "parameters": [face, fidx, 0, 2, ""]}]
        for line in lines:
            result.append({"code": 401, "indent": 0, "parameters": [line]})
        result.append({"code": 0, "indent": 0, "parameters": []})
        return result

    page1 = {
        "conditions": {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False,
            "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
            "variableId": 1, "variableValid": False, "variableValue": 0
        },
        "directionFix": True,
        "image": {
            "characterIndex": face_index % 4,
            "characterName": "People1",
            "direction": direction,
            "pattern": 1,
            "tileId": 0
        },
        "list": build_message_list(lines_page1, face_name, face_index) if not lines_page2 else
                build_message_list(lines_page1, face_name, face_index) + [{"code": 123, "indent": 0, "parameters": ["A", 0]}] + [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
        "moveSpeed": 3,
        "moveType": 0,
        "priorityType": 1,
        "stepAnime": False,
        "through": False,
        "trigger": 0,
        "walkAnime": True
    }

    # 初回セリフ + セルフスイッチON
    page1["list"] = build_message_list(lines_page1, face_name, face_index)
    if lines_page2:
        # セルフスイッチをONにするコマンドを末尾に追加
        page1["list"].insert(-1, {"code": 123, "indent": 0, "parameters": ["A", 0]})

    pages = [page1]

    if lines_page2:
        page2 = {
            "conditions": {
                "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": True,
                "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                "variableId": 1, "variableValid": False, "variableValue": 0
            },
            "directionFix": True,
            "image": {
                "characterIndex": face_index % 4,
                "characterName": "People1",
                "direction": direction,
                "pattern": 1,
                "tileId": 0
            },
            "list": build_message_list(lines_page2, face_name, face_index),
            "moveFrequency": 3,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 1,
            "stepAnime": False,
            "through": False,
            "trigger": 0,
            "walkAnime": True
        }
        pages.append(page2)

    return {"id": event_id, "name": name, "note": "", "x": x, "y": y, "pages": pages}


def make_sign_event(event_id, name, x, y, lines):
    """看板イベントを作成（会話なし、メッセージのみ）"""
    msg_list = [{"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]}]
    for line in lines:
        msg_list.append({"code": 401, "indent": 0, "parameters": [line]})
    msg_list.append({"code": 0, "indent": 0, "parameters": []})

    return {
        "id": event_id,
        "name": name,
        "note": "",
        "x": x,
        "y": y,
        "pages": [{
            "conditions": {
                "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
                "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False,
                "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
                "variableId": 1, "variableValid": False, "variableValue": 0
            },
            "directionFix": True,
            "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
            "list": msg_list,
            "moveFrequency": 3,
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3,
            "moveType": 0,
            "priorityType": 0,
            "stepAnime": False,
            "through": False,
            "trigger": 0,
            "walkAnime": False
        }]
    }


# ============================================================
# Map001 にNPC・看板を追加
# ============================================================
path1 = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map001.json'
shutil.copy(path1, path1 + '.bak_story')
with open(path1, 'r', encoding='utf-8') as f:
    m1 = json.load(f)

existing_ids = [e['id'] for e in m1['events'] if e]
next_id = max(existing_ids) + 1

# NPC①: 村人のおじさん（ガイド役）
m1['events'].append(make_npc_event(
    next_id, "村人のおじさん", 3, 4,
    lines_page1=[
        "おお、旅人よ！ようこそオノマトペ村へ！",
        "この村では「音」に宿る力を武器にするんじゃ。",
        "東の洞窟には強い魔物がおる。",
        "オノマトペ武器を手に入れてから行くといいぞ！"
    ],
    lines_page2=[
        "オノマトペ武器…ちゃんと手に入れたかの？",
        "洞窟の奥には、まだ誰も見たことのない",
        "「究極のオノマトペ」が眠っているとの噂じゃ。"
    ],
    face_name="", face_index=0, direction=2
))
next_id += 1

# NPC②: オノマトペ研究者
m1['events'].append(make_npc_event(
    next_id, "オノマトペ研究者", 10, 6,
    lines_page1=[
        "やぁ！私はオノマトペ兵器の研究者です！",
        "「ドカバキハンマー」は打撃音を増幅させ",
        "「シュバシュバ刀」は斬撃音で敵を翻弄します。",
        "「ゴロゴロ杖」は雷鳴の轟きを魔法に変換！"
    ],
    lines_page2=[
        "オノマトペ武器は、音の強さで威力が変わります。",
        "大声で攻撃するとより強力になるかも…？",
        "…というのは冗談ですよ（笑）"
    ],
    face_name="", face_index=1, direction=2
))
next_id += 1

# NPC③: 不安な少女
m1['events'].append(make_npc_event(
    next_id, "不安な少女", 8, 9,
    lines_page1=[
        "…ねえ、お兄さん（お姉さん）。",
        "もしかして、洞窟に行くの…？",
        "お父さんが昨日から帰ってこないの。",
        "お願い…探してきてくれませんか…？"
    ],
    lines_page2=[
        "…お父さん、まだ帰ってきてないの。",
        "洞窟の奥に…いるのかな…。",
        "ねえ、助けてあげて……"
    ],
    face_name="", face_index=2, direction=2
))
next_id += 1

# 看板①: 村の看板
m1['events'].append(make_sign_event(
    next_id, "看板（村の入り口）", 6, 2,
    lines=[
        "★ オノマトペ村へようこそ ★",
        "ここは「音の力」が宿る武器を生み出す村。",
        "勇者たちよ、オノマトペと共に戦え！"
    ]
))
next_id += 1

# 看板②: 洞窟警告看板
m1['events'].append(make_sign_event(
    next_id, "看板（洞窟警告）", 14, 5,
    lines=[
        "⚠ 危険 ⚠",
        "この先、魔物の巣窟「ゴロゴロ洞窟」。",
        "オノマトペ武器なき者、立ち入るべからず！"
    ]
))
next_id += 1

with open(path1, 'w', encoding='utf-8', newline='') as f:
    json.dump(m1, f, ensure_ascii=False, separators=(',', ':'))

print("✅ Map001 NPC・看板追加完了！")
print(f"  追加イベント数: 5個")
print(f"  総イベント数: {len([e for e in m1['events'] if e])}")


# ============================================================
# Map002 に旅人・石碑・入場演出を追加
# ============================================================
path2 = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data\Map002.json'
shutil.copy(path2, path2 + '.bak_story')
with open(path2, 'r', encoding='utf-8') as f:
    m2 = json.load(f)

existing_ids2 = [e['id'] for e in m2['events'] if e]
next_id2 = max(existing_ids2) + 1

# NPC④: 迷い込んだ旅人
m2['events'].append(make_npc_event(
    next_id2, "迷い込んだ旅人", 3, 8,
    lines_page1=[
        "ゼェッ…ゼェッ…た、助かった…！",
        "この洞窟、迷子になったらヤバいぞ！",
        "出口は南の方にあるはず…",
        "早く脱出しないと、魔物に…！"
    ],
    lines_page2=[
        "おう、まだいたのか。",
        "俺は…ちょっと休んでから帰るよ。",
        "奥には気をつけろよ。ボスがいる気がする…"
    ],
    face_name="", face_index=3, direction=2
))
next_id2 += 1

# NPC⑤: 洞窟の石碑（謎めいたメッセージ）
m2['events'].append(make_sign_event(
    next_id2, "洞窟の石碑", 10, 4,
    lines=[
        "《古代文字》",
        "ゴロゴロ、ドカバキ、シュバシュバ、ピカピカ…",
        "四つの音が揃いし時、",
        "洞窟の扉は永遠に開かれん。"
    ]
))
next_id2 += 1

# 演出: 洞窟入場時フラッシュ（地形タッチで自動実行）
entrance_event = {
    "id": next_id2,
    "name": "洞窟入場演出",
    "note": "",
    "x": 8, "y": 12,
    "pages": [{
        "conditions": {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False,
            "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
            "variableId": 1, "variableValid": False, "variableValue": 0
        },
        "directionFix": False,
        "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
        "list": [
            # 画面フラッシュ（赤っぽい洞窟の雰囲気）
            {"code": 223, "indent": 0, "parameters": [{"r": 0, "g": 0, "b": 0, "a": 128}, 30, False]},
            # テキスト表示
            {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
            {"code": 401, "indent": 0, "parameters": ["（洞窟の中は薄暗く、不気味な音が響く…）"]},
            {"code": 401, "indent": 0, "parameters": ["…ゴロゴロ……"]},
            # 画面を元に戻す
            {"code": 223, "indent": 0, "parameters": [{"r": 0, "g": 0, "b": 0, "a": 0}, 30, False]},
            # セルフスイッチON（初回のみ）
            {"code": 123, "indent": 0, "parameters": ["A", 0]},
            {"code": 0, "indent": 0, "parameters": []}
        ],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
        "moveSpeed": 3,
        "moveType": 0,
        "priorityType": 0,
        "stepAnime": False,
        "through": True,
        "trigger": 2,  # プレイヤーに触れた時
        "walkAnime": False
    },{
        # 2回目以降は何もしない
        "conditions": {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False,
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": True,
            "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False,
            "variableId": 1, "variableValid": False, "variableValue": 0
        },
        "directionFix": False,
        "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
        "list": [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
        "moveSpeed": 3,
        "moveType": 0,
        "priorityType": 0,
        "stepAnime": False,
        "through": True,
        "trigger": 2,
        "walkAnime": False
    }]
}
m2['events'].append(entrance_event)
next_id2 += 1

# マップ名を設定（まだ設定されていなければ）
if not m2.get('displayName'):
    m2['displayName'] = 'ゴロゴロ洞窟'

with open(path2, 'w', encoding='utf-8', newline='') as f:
    json.dump(m2, f, ensure_ascii=False, separators=(',', ':'))

print("✅ Map002 旅人・石碑・演出追加完了！")
print(f"  追加イベント数: 3個")
print(f"  総イベント数: {len([e for e in m2['events'] if e])}")
print()
print("🎉 すべてのストーリーイベント追加完了！")
