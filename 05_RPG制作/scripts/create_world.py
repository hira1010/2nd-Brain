import json
import os

# =========================================================================
# CONFIGURATION
# =========================================================================

DATA_DIR = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\data'
OPENING_SWITCH = 10 # オープニング終了判定に使うスイッチ番号

# =========================================================================
# UTILITY FUNCTIONS
# =========================================================================

def build_events_array(event_list):
    """
    イベントのリストを、IDインデックスベースの配列（JSON仕様）に変換します。
    """
    max_id = max([e["id"] for e in event_list]) if event_list else 0
    arr = [None] * (max_id + 1)
    for e in event_list:
        arr[e["id"]] = e
    return arr

def save_map(map_id, name, width, height, tileset_id, events, default_tile=2816):
    """
    指定されたパラメータとイベントリストを用いてマップ(JSON)を保存します。
    """
    map_path = os.path.join(DATA_DIR, f'Map{map_id:03d}.json')
    map_obj = {
        "autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "",
        "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90}, 
        "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "disableDashing": False, "displayName": name, "encounterList": [], "encounterStep": 30,
        "height": height, "note": "", "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": "",
        "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0, "specifyBattleback": False,
        "tilesetId": tileset_id, "width": width, 
        "data": [default_tile] * (width * height) + [0] * (width * height * 5),
        "events": build_events_array(events)
    }
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(map_obj, f, ensure_ascii=False, indent=2)

# =========================================================================
# EVENT GENERATORS
# =========================================================================

def create_base_event(event_id, name, x, y, list_commands, note="", trigger=0, move_type=0, character_name="", character_index=0, conditions=None):
    """
    基礎的なイベントオブジェクトを生成します。
    """
    if conditions is None:
        conditions = {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False, 
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, 
            "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, 
            "variableId": 1, "variableValid": False, "variableValue": 0
        }
        
    return {
        "id": event_id, "name": name, "note": note, "x": x, "y": y,
        "pages": [{
            "conditions": conditions,
            "directionFix": False,
            "image": {"characterIndex": character_index, "characterName": character_name, "direction": 2, "pattern": 1, "tileId": 0},
            "list": list_commands + [{"code": 0, "indent": 0, "parameters": []}],
            "moveFrequency": 3, 
            "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
            "moveSpeed": 3, "moveType": move_type, "priorityType": 1, "stepAnime": False, "through": False, 
            "trigger": trigger, "walkAnime": True
        }]
    }

def create_chest_event(event_id, x, y, item_id, item_name):
    """
    宝箱イベントを生成します。
    """
    commands = [
        {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
        {"code": 401, "indent": 0, "parameters": ["宝箱を開けた！"]},
        {"code": 224, "indent": 0, "parameters": [[255, 255, 255, 128], 60, True]},
        {"code": 250, "indent": 0, "parameters": [{"name": "Powerup", "volume": 90, "pitch": 100, "pan": 0}]},
        {"code": 127, "indent": 0, "parameters": [item_id, 0, 0, 1, False]},
        {"code": 401, "indent": 0, "parameters": [f"【{item_name}】を手に入れた！"]},
        {"code": 123, "indent": 0, "parameters": ["A", 0]}
    ]
    return create_base_event(event_id, "Chest", x, y, commands, character_name="!Chest")

def create_transfer_event(event_id, name, x, y, dest_map_id, dest_x, dest_y):
    """
    マップ間の移動（Exit）イベントを生成します。
    """
    commands = [{"code": 201, "indent": 0, "parameters": [0, dest_map_id, dest_x, dest_y, 0, 0]}]
    return create_base_event(event_id, name, x, y, commands, trigger=1)

def create_enemy_event(event_id, x, y):
    """
    通常敵イベントを生成します（実際の動作制御はABS_Ultimate.js側で行うためコマンドは空）。
    """
    return create_base_event(event_id, "Enemy", x, y, [], note="<Enemy>", character_name="Monster", move_type=1)

def create_startup_event(event_id):
    """
    ゲーム開始時に一度だけ実行されるオープニングイベント（v6.1 超安定版）を生成します。
    """
    # ページ1 (初期実行 - オートラン)
    page1 = {
        "conditions": {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False, 
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, 
            "switch1Id": OPENING_SWITCH, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, 
            "variableId": 1, "variableValid": False, "variableValue": 0
        },
        "directionFix": False, "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
        "list": [
            # ----- 致命的バグ回避レイヤー（画面非表示系の強制リセット） -----
            {"code": 222, "indent": 0, "parameters": []}, # FADE IN
            {"code": 223, "indent": 0, "parameters": [[0, 0, 0, 0], 1, True]}, # TINT NORMAL
            {"code": 211, "indent": 0, "parameters": [1]}, # TRANSPARENCY OFF (params[0] == 1 means false)
            {"code": 355, "indent": 0, "parameters": ["if(typeof Graphics !== 'undefined') Graphics.showScreen();"]},
            
            # ----- 動画再生 -----
            {"code": 261, "indent": 0, "parameters": ["0320"]}, # PLAY VIDEO
            
            # ----- 初期化処理とストーリーテリング -----
            {"code": 355, "indent": 0, "parameters": ["ABS.setupInitialState();"]},
            {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
            {"code": 401, "indent": 0, "parameters": ["この世には７つのオノマトペがある。"]},
            {"code": 401, "indent": 0, "parameters": ["それをそろえたとき、最高の美女動画がみれるという……。"]},
            {"code": 230, "indent": 0, "parameters": [10]},
            
            # ----- 操作説明（ネイティブメッセージ利用による安定化） -----
            {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
            {"code": 401, "indent": 0, "parameters": ["\\C[16]【操作ガイド】\\C[0]"]},
            {"code": 401, "indent": 0, "parameters": ["この世界は \\C[1]ZまたはEnterキー\\C[0] で攻撃できます。"]},
            {"code": 401, "indent": 0, "parameters": ["手に入れたオノマトペは \\C[1]Shiftキー\\C[0] で切り替えられます。"]},
            {"code": 401, "indent": 0, "parameters": ["まずは近くの敵を倒しにいこう！"]},
            
            # ----- 念のためのクリーンアップと終了処理 -----
            {"code": 355, "indent": 0, "parameters": ["if(typeof Video !== 'undefined' && Video._element) { Video._element.style.display = 'none'; Video._element.style.pointerEvents = 'auto'; }"]},
            {"code": 355, "indent": 0, "parameters": ["if(typeof Graphics !== 'undefined') Graphics.showScreen();"]},
            {"code": 121, "indent": 0, "parameters": [OPENING_SWITCH, OPENING_SWITCH, 0]},
            {"code": 0, "indent": 0, "parameters": []}
        ],
        "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}, 
        "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 3, "walkAnime": True
    }
    
    # ページ2 (オープニング終了後 - 殻イベント)
    page2 = {
        "conditions": {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False, 
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, 
            "switch1Id": OPENING_SWITCH, "switch1Valid": True, "switch2Id": 1, "switch2Valid": False, 
            "variableId": 1, "variableValid": False, "variableValue": 0
        },
        "directionFix": False, "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
        "list": [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}, 
        "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 0, "walkAnime": True
    }
    
    return {
        "id": event_id, "name": "Startup", "note": "", "x": 0, "y": 0, "pages": [page1, page2]
    }


# =========================================================================
# MAP CONSTRUCTION
# =========================================================================

def build_map_001_grassland():
    events = [
        create_chest_event(1, 2, 2, 51, "ピカピカ剣"),
        create_chest_event(2, 2, 4, 39, "ドドドの極意"),
        create_chest_event(7, 4, 2, 45, "オノマトペ強化の極意"), # NEW: Reinforce Item
        create_transfer_event(3, "Exit", 16, 6, 2, 1, 6),
        create_enemy_event(4, 10, 5),
        create_enemy_event(5, 12, 8),
        create_startup_event(6)
    ]
    save_map(1, "平原", 17, 13, 1, events)

def build_map_002_forest():
    events = [
        create_chest_event(1, 5, 2, 40, "ドキドキの極意"),
        create_chest_event(2, 12, 10, 41, "ふわっの極意"),
        create_transfer_event(3, "Exit_L", 0, 6, 1, 15, 6),
        create_transfer_event(4, "Exit_R", 16, 6, 3, 1, 6),
        create_enemy_event(5, 8, 6),
        create_enemy_event(6, 4, 3),
        create_enemy_event(7, 13, 8)
    ]
    save_map(2, "森", 17, 13, 2, events)

def build_map_003_mountain():
    events = [
        create_chest_event(1, 8, 2, 42, "ちゅちゅの極意"),
        create_chest_event(2, 4, 10, 43, "きゅんの極意"),
        create_transfer_event(3, "Exit_L", 0, 6, 2, 15, 6),
        create_transfer_event(4, "Exit_R", 16, 6, 4, 1, 6),
        create_enemy_event(5, 10, 10),
        create_enemy_event(6, 6, 4)
    ]
    save_map(3, "山", 17, 13, 3, events)

def build_map_004_cave():
    events = [
        create_chest_event(1, 3, 3, 44, "わくわくの極意"),
        create_transfer_event(2, "Exit_L", 0, 6, 3, 15, 6),
        create_base_event(3, "Boss", 14, 6, [
            {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
            {"code": 401, "indent": 0, "parameters": ["ククク……よくここまで辿り着いたな。"]},
            {"code": 401, "indent": 0, "parameters": ["ここで死ぬがいい！"]}
        ], note="<Boss>", character_name="Evil", character_index=0, move_type=1)
    ]
    
    # Boss Defeated Page
    events[2]["pages"].append({
        "conditions": {
            "actorId": 1, "actorValid": False, "enemyIndex": 0, "enemyValid": False, 
            "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": True, 
            "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, 
            "variableId": 1, "variableValid": False, "variableValue": 0
        },
        "directionFix": False, "image": {"characterIndex": 0, "characterName": "", "direction": 2, "pattern": 1, "tileId": 0},
        "list": [
            {"code": 101, "indent": 0, "parameters": ["", 0, 0, 2, ""]},
            {"code": 401, "indent": 0, "parameters": ["バ、バカな……！"]},
            {"code": 121, "indent": 0, "parameters": [2, 2, 0]}, # Boss Defeated Switch (e.g., Switch 2)
            {"code": 0, "indent": 0, "parameters": []}
        ], 
        "moveFrequency": 3, "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False}, 
        "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False, "trigger": 3, "walkAnime": True
    })
    
    save_map(4, "洞窟", 17, 13, 5, events)

# =========================================================================
# MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":
    build_map_001_grassland()
    build_map_002_forest()
    build_map_003_mountain()
    build_map_004_cave()
    print("Ultimate World Expanded (v7.0) - Refactored Configuration Successfully Built.")
