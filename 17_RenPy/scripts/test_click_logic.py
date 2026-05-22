# scripts/test_click_logic.py
# ヒロインクリック機能のロジック検証用スクリプト

import sys

# ---------------------------------------------------------
# 1. Ren'py環境のシミュレーター (Mock)
# ---------------------------------------------------------
class MockRenpy:
    def __init__(self):
        self.shown_screens = []
        self.played_sounds = []
        self.restarts = 0

    def get_mouse_pos(self):
        return (640, 360) # テスト用のマウス位置

    def show_screen(self, name, **kwargs):
        self.shown_screens.append((name, kwargs))

    def play(self, path, channel):
        self.played_sounds.append((path, channel))

    def restart_interaction(self):
        self.restarts += 1

# モックをセット
renpy = MockRenpy()

# ---------------------------------------------------------
# 2. テスト対象の変数と関数 (提供されたコード)
# ---------------------------------------------------------

p_intimacy = 0.0
p_pleasure = 0.0
p_rank = 1
p_shake_type = None 
VOICE_DIR = "C:/Users/hirak/Desktop/eroge音声/"

def click_action(part):
    global p_intimacy, p_pleasure, p_rank, p_shake_type
    
    # ハートを表示
    m_pos = renpy.get_mouse_pos()
    renpy.show_screen("heart_layer", x=m_pos[0], y=m_pos[1])

    v_file = ""
    p_shake_type = None 

    if part == "ear":
        p_intimacy += 1.5
        v_file = "ear.wav"
        p_shake_type = "shiver" 
    elif part == "chest":
        p_intimacy += 2.0
        p_pleasure += 5.0
        v_file = "chest.wav"
        p_shake_type = "shake" 
    elif part == "crotch":
        p_intimacy += 5.0
        p_pleasure += 10.0
        v_file = "crotch.wav"
        p_shake_type = "shiver"

    if v_file:
        renpy.play(VOICE_DIR + v_file, channel="voice")

    if p_intimacy > 100: p_rank = 3
    elif p_intimacy > 40: p_rank = 2

    renpy.restart_interaction()

# ---------------------------------------------------------
# 3. 検証実行 (Test Cases)
# ---------------------------------------------------------

def run_tests():
    global p_intimacy, p_pleasure, p_rank, p_shake_type
    
    print("--- 🔄 ヒロインクリック機能 テスト開始 ---")
    
    # テスト1: 耳をクリック
    print("\n[テスト1] 耳をクリック")
    click_action("ear")
    assert p_intimacy == 1.5, f"❌ 耳: 好感度アップ失敗 (現在: {p_intimacy})"
    assert p_shake_type == "shiver", "❌ 耳: 揺れタイプ設定失敗"
    assert any(s[0] == "heart_layer" for s in renpy.shown_screens), "❌ ハート表示失敗"
    print("✅ 合格: 耳のクリックOK")

    # テスト2: 胸をクリック
    print("\n[テスト2] 胸をクリック")
    prev_int = p_intimacy
    click_action("chest")
    assert p_intimacy == prev_int + 2.0, "❌ 胸: 好感度アップ失敗"
    assert p_pleasure == 5.0, "❌ 胸: 快楽度アップ失敗"
    assert p_shake_type == "shake", "❌ 胸: 揺れタイプ設定失敗"
    print("✅ 合格: 胸のクリックOK")

    # テスト3: ランクアップ判定 (Rank 2)
    print("\n[テスト3] ランク2への昇格判定")
    p_intimacy = 39.0
    click_action("ear") # +1.5 -> 40.5
    assert p_rank == 2, f"❌ ランク2への昇格失敗 (好感度: {p_intimacy})"
    print("✅ 合格: ランク2への昇格OK")

    # テスト4: ランクアップ判定 (Rank 3)
    print("\n[テスト4] ランク3への昇格判定")
    p_intimacy = 99.0
    click_action("ear") # +1.5 -> 100.5
    assert p_rank == 3, f"❌ ランク3への昇格失敗 (好感度: {p_intimacy})"
    print("✅ 合格: ランク3への昇格OK")

    print("\n🎉 全てのテストに合格しました！")

if __name__ == "__main__":
    try:
        run_tests()
    except AssertionError as e:
        print(f"\n❌ テスト失敗: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n☢️ 予期せぬエラー: {e}")
        sys.exit(1)
