# screens.rpy - Ver 7.2 安定性重視版

# ==========================================
# 3. メイン画面 (Screen)
# ==========================================

screen main_interaction(shake=False):
    # 背景の表示
    add "bg_classroom"

    # ヒロイン表示（胸クリック時は揺れる演出）
    if shake:
        add "heroine_main" at breast_shake
        # 0.2秒後に揺れを止めるために自分自身を再表示
        timer 0.2 action Show("main_interaction", shake=False)
    else:
        add "heroine_main"

    # ステータス表示（左上）
    frame:
        background Solid("#00000088")
        padding (10, 10)
        align (0.05, 0.05)
        vbox:
            text "Rank: [p_rank]" size 30 color "#ff69b4"
            text "Love (親密度): [p_intimacy:.1f]"
            text "Pleasure (快感度): [p_pleasure:.1f] / 100"
            text "Money: [p_money] Yen"

    # 部位別当たり判定
    
    # 耳
    imagebutton:
        idle Solid("#0000", xsize=150, ysize=150)
        # 一撃必殺：すべての動作（計算・座標取得・波紋・揺れ）を Python 関数で実行
        action [Function(trigger_click_action, "ear"), 
                Play("voice", VOICE_DIR + "ear.wav")]
        pos (570, 100)

    # 胸
    imagebutton:
        idle Solid("#0000", xsize=280, ysize=200)
        action [Function(trigger_click_action, "chest"), 
                Play("voice", VOICE_DIR + "chest.wav")]
        pos (510, 270)

    # 股間
    imagebutton:
        idle Solid("#0000", xsize=180, ysize=200)
        action [Function(trigger_click_action, "crotch"), 
                Play("voice", VOICE_DIR + "crotch.wav")]
        pos (550, 570)

    # 下部メニュー
    hbox:
        align (0.5, 0.95)
        spacing 50
        textbutton "チェキ撮影" action Jump("take_photo")
        textbutton "ショップ" action Jump("open_shop")

# ==========================================
# 4. 演出用スクリーン (Effects)
# ==========================================

screen ripple_screen(mpos):
    zorder 100
    # 波紋エフェクト：マウス座標に半透明の白い丸を表示
    # Transient属性により表示後すぐに消えるようにし、メモリ残りを防ぎます
    add Solid("#ffffff88", xsize=60, ysize=60) at ripple_effect:
        pos mpos
        anchor (0.5, 0.5)
    
    # 演出が完了したら自分自身を閉じる（念のための強制終了）
    timer 0.6 action Hide("ripple_screen")
