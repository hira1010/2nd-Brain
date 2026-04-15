# logic.rpy - Ver 8.0 密着クリック＆チェキ経済版

init python:
    import random

    # 音声フォルダのパス
    # ※ユーザー様のデスクトップにある音声フォルダを参照
    VOICE_DIR = "C:/Users/hirak/Desktop/eroge音声/"

    def calculate_click(part_key):
        global p_intimacy, p_pleasure, p_rank, p_anger, is_punishment
        
        # 指定された部位の設定を取得
        cfg = PARTS_CONFIG.get(part_key)
        if not cfg:
            return

        # 連続クリックによる怒り判定（簡易版）
        p_anger += 1
        if p_anger > 15:
            # 怒り爆発：お仕置きラベルへ強制移動
            renpy.jump("punishment_start")
            return

        # 基礎上昇値を設定から取得
        inc_int = cfg.get("inc_int", 0.0)
        inc_ple = cfg.get("inc_ple", 0.0)
        
        # 胸などの揺れ演出が必要な場合
        if cfg.get("shake", False):
            renpy.show_screen("main_interaction", shake=True)

        # 装備品による倍率補正
        int_mult = 1.5 if has_ribbon else 1.0
        ple_mult = 2.0 if has_perfume else 1.0

        # 変数更新 (微量のランダム値を加算して飽きを防止)
        p_intimacy += (inc_int + random.uniform(0, 1.0)) * int_mult
        p_pleasure += (inc_ple + random.uniform(0, 2.0)) * ple_mult

        # ランク更新判定
        if p_intimacy > 100:
            p_rank = 3
        elif p_intimacy > 40:
            p_rank = 2
        
        # 画面の再描画を促す
        renpy.restart_interaction()

    # クリック時の演出と数値を一括で制御する関数
    def trigger_click_action(part):
        # 1. 現在のマウス位置（クリックした場所）を取得
        mpos = renpy.get_mouse_pos()
        
        # 2. 波紋エフェクトを表示
        renpy.show_screen("ripple_screen", mpos=mpos)
        
        # 3. 実際の数値計算と揺れ演出の呼び出し
        calculate_click(part)
