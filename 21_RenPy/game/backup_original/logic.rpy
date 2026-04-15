# logic.rpy - Ver 7.0 密着クリック＆チェキ経済版

init python:
    import random

    # 音声フォルダのパス
    # ※ユーザー様のデスクトップにある音声フォルダを参照
    VOICE_DIR = "C:/Users/hirak/Desktop/eroge音声/"

    # クリック時の処理（新：演出・数値・アイテム効果統合版）
    def click_action(part):
        global p_intimacy, p_pleasure, p_rank, p_shake_type, p_anger
        
        # 1. ハートエフェクト（クリック位置に表示）
        m_pos = renpy.get_mouse_pos()
        renpy.show_screen("heart_layer", x=m_pos[0], y=m_pos[1])

        # 2. 連続クリックによる怒り判定（既存機能）
        p_anger += 1
        if p_anger > 20: # 許容回数を少し緩和
            renpy.jump("punishment_start")
            return

        v_file = ""
        p_shake_type = None 

        # 3. 装備品による倍率補正（既存機能）
        int_mult = 1.5 if has_ribbon else 1.0
        ple_mult = 2.0 if has_perfume else 1.0

        # 4. 部位ごとの数値加算（提供ロジック適用）
        if part == "ear":
            p_intimacy += 1.5 * int_mult
            v_file = "ear.wav"
            p_shake_type = "shiver" 
        elif part == "chest":
            p_intimacy += 2.0 * int_mult
            p_pleasure += 5.0 * ple_mult
            v_file = "chest.wav"
            p_shake_type = "shake" 
        elif part == "crotch":
            p_intimacy += 5.0 * int_mult
            p_pleasure += 10.0 * ple_mult
            v_file = "crotch.wav"
            p_shake_type = "shiver"

        # 5. 音声再生
        if v_file:
            renpy.play(VOICE_DIR + v_file, channel="voice")

        # 6. ランク更新判定
        if p_intimacy > 100:
            p_rank = 3
        elif p_intimacy > 40:
            p_rank = 2

        # 7. 画面の再描画
        renpy.restart_interaction()
