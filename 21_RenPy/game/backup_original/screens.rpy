# screens.rpy - Ver 7.2 安定性重視版

# ==========================================
# 3. メイン画面 (Screen)
# ==========================================

screen main_interaction():
    # 背景の表示
    add "bg_classroom"

    # ヒロイン表示（演出タイプによってアニメーションを切り替え）
    if p_shake_type == "shake":
        add "heroine_main" at breast_shake
        timer 0.2 action SetVariable("p_shake_type", None)
    elif p_shake_type == "shiver":
        add "heroine_main" at body_shiver
        timer 0.2 action SetVariable("p_shake_type", None)
    else:
        add "heroine_main" at bottom_center # 通常時も中央下固定

    # ステータス表示（左上）
    frame:
        background Solid("#00000088")
        padding (10, 10)
        align (0.05, 0.05)
        vbox:
            spacing 10
            text "ヒロインの状態" size 20 color "#aaa"
            text "Rank: [p_rank]" size 35 color "#ff69b4" outlines [(2, "#fff", 0, 0)]
            
            null height 10
            text "Love (親密度): [p_intimacy:.1f]" size 22
            
            vbox:
                text "Pleasure (快感度)" size 18 color "#ffb6c1"
                bar value p_pleasure range 100 xsize 300 ysize 25:
                    left_bar Frame(Solid("#ff1493"), 4, 4)
                    right_bar Frame(Solid("#444"), 4, 4)
            
            null height 10
            hbox:
                text "所持金: " size 24
                text "¥ [p_money:,]" size 28 color "#ffd700" bold True

    # --- 当たり判定（完全に透明） ---
    # 耳
    imagebutton:
        idle Solid("#00000000")
        xysize (100, 100)
        action Function(click_action, "ear")
        pos (610, 140) # 640x360からの比率で微調整

    # 胸
    imagebutton:
        idle Solid("#00000000")
        xysize (250, 150)        
        action Function(click_action, "chest")
        pos (520, 270)          

    # 股間
    imagebutton:
        idle Solid("#00000000")
        xysize (180, 200)       
        action Function(click_action, "crotch")
        pos (560, 570)          

    # 下部メニュー
    hbox:
        align (0.5, 0.95)
        spacing 50
        textbutton "チェキ撮影" action Jump("take_photo")
        textbutton "ショップ" action Jump("open_shop")

# ==========================================
# 4. 演出用スクリーン (Effects)
# ==========================================

screen heart_layer(x, y):
    zorder 101 # ヒロインより前面
    add "heart_particle" at heart_float(x, y)
    timer 0.8 action Hide("heart_layer")

screen ripple_screen(mpos):
    zorder 100
    add Solid("#ffffff88", xsize=60, ysize=60) at ripple_effect:
        pos mpos
        anchor (0.5, 0.5)
    timer 0.6 action Hide("ripple_screen")
