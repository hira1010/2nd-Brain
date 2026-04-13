import os
import sys
import re

# -----------------------------------------------------------------------------
# 1. Ren'Py 環境のモック (Mocking)
# -----------------------------------------------------------------------------
class RenpyMock:
    def __init__(self):
        self.notifies = []
        self.played_audio = []
        self.shown_screens = []
        self.restarts = 0
        self.jump_target = None
    def notify(self, msg): self.notifies.append(msg)
    def play(self, target, channel="sound"): self.played_audio.append((target, channel))
    def show_screen(self, name, *args, **kwargs): self.shown_screens.append(name)
    def restart_interaction(self): self.restarts += 1
    def get_mouse_pos(self): return (640, 360) 
    def list_files(self): return []
    def jump(self, label): self.jump_target = label

# グローバルなモックをセット
renpy = RenpyMock()

# -----------------------------------------------------------------------------
# 2. logic.rpy の読み込みと実行
# -----------------------------------------------------------------------------
def run_logic_tests():
    print("--- 🔄 HeroineAdv Engine Logic Test (Ver 7.0 Full Spec) ---")
    
    # 疑似的なグローバル名前空間
    namespace = {
        "renpy": renpy,
        "VOICE_DIR": "C:/mock/voice/",
        "has_ribbon": False,
        "has_perfume": False,
        "has_lens": False,
        "p_intimacy": 0.0,
        "p_pleasure": 0.0,
        "p_rank": 1,
        "p_money": 0,
        "p_anger": 0,
    }

    # logic.rpy を解析して Python ブロックを抽出
    logic_path = "game/logic.rpy"
    if not os.path.exists(logic_path):
        print("❌ Error: logic.rpy not found")
        return False

    with open(logic_path, "r", encoding="utf-8") as f:
        content = f.read()

    # init python ブロックの抽出
    blocks = re.findall(r"init python:\n((?:    .*\n| *\n)+)", content)
    for block in blocks:
        clean_block = "\n".join([line[4:] if line.startswith("    ") else line for line in block.split("\n")])
        try:
            exec(clean_block, namespace)
        except Exception as e:
            print(f"❌ Error in logic.rpy code block: {e}")
            return False

    # -------------------------------------------------------------------------
    # 3. 具体的なテストケース
    # -------------------------------------------------------------------------
    results = []

    def assert_test(name, condition):
        if condition:
            print(f"✅ PASS: {name}")
            results.append(True)
        else:
            print(f"❌ FAIL: {name}")
            results.append(False)

    # テストA: 初期状態
    assert_test("Initial p_pleasure is 0", namespace["p_pleasure"] == 0)
    assert_test("Initial p_intimacy is 0", namespace["p_intimacy"] == 0)

    # テストB: 部位クリック (Ear)
    namespace["calculate_click"]("ear")
    assert_test("Ear click increases intimacy", namespace["p_intimacy"] > 0)
    assert_test("Anger increases by click", namespace["p_anger"] == 1)

    # テストC: 胸クリック (Chest)
    current_p = namespace["p_pleasure"]
    namespace["calculate_click"]("chest")
    assert_test("Chest click increases pleasure", namespace["p_pleasure"] > current_p)
    assert_test("Chest click shows interaction screen (jiggle)", "main_interaction" in renpy.shown_screens)

    # テストD: お仕置き判定
    namespace["p_anger"] = 15
    namespace["calculate_click"]("ear")
    assert_test("Anger > 15 triggers punishment jump", renpy.jump_target == "punishment_start")

    # テストE: 装備品効果 (Ribbon)
    namespace["p_intimacy"] = 0
    namespace["p_anger"] = 0
    renpy.jump_target = None
    namespace["has_ribbon"] = True
    namespace["calculate_click"]("ear")
    # inc_int = 1.0, mult = 1.5, random = 0~1. -> Result should be >= 1.5
    assert_test("Ribbon (multiplier 1.5) works", namespace["p_intimacy"] >= 1.5)




    # テストF: アセット整合性
    print("\n--- 📁 Asset Integrity Check ---")
    required_images = [
        "game/images/heroine_rank1.png",
        "game/images/heroine_rank2.png",
        "game/images/heroine_rank3.png",
        "game/images/bg classroom_day.png"
    ]
    for img in required_images:
        found = os.path.exists(img)
        assert_test(f"Check Asset: {os.path.basename(img)}", found)

    # 4. 最終判定
    if all(results):
        print("\n🎉 ALL TESTS PASSED (GREEN)")
        return True
    else:
        print("\n😱 SOME TESTS FAILED (RED)")
        return False

if __name__ == "__main__":
    if run_logic_tests():
        sys.exit(0)
    else:
        sys.exit(1)

