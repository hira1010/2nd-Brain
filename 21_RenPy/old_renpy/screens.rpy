# インターフェース定義 (製品版・安定動作モデル)

screen interaction():
    tag interaction
    zorder 100
    
    # --- 1. エフェクト更新タイマー (60FPS相当で滑らかに) ---
    timer 0.02 repeat True action Function(update_effects)

    # --- 2. 描画: 背景 ---
    add "bg classroom_day"

    # --- 3. 描画: ヒロイン (ランクに応じて自動切り替え) ---
    # 画像定義側で zoom/yalign が設定されているため、横位置のみ指定
    add "heroine_rank[intimacy_rank]" xalign 0.5

    # --- 4. 描画: インゲーム・エフェクト ---
    for e in active_effects:
        $ alpha_val = e.life / e.max_life
        if e.etype == "star":
            text "⭐" pos (int(e.x), int(e.y)) size 80 outlines [(2, "#000", 0, 0)] at Transform(alpha=alpha_val, rotate=e.rotation)
        else:
            text "❤️" pos (int(e.x), int(e.y)) size 100 outlines [(2, "#fff", 0, 0)] at Transform(alpha=alpha_val, rotate=e.rotation)

    # --- 5. ステータス表示 (HUD) ---
    frame:
        background Solid("#0008")
        padding (20, 15)
        xalign 0.0 yalign 0.0
        xsize 320
        has vbox:
            spacing 8
            vbox:
                spacing 2
                text "親密度: [persistent.intimacy] / [goal_intimacy]" size 24 color "#ff99cc"
                bar value persistent.intimacy range goal_intimacy xsize 280 ysize 10 left_bar Solid("#ff99cc") right_bar Solid("#444")
            text "所持金: [persistent.money]円" size 22 color "#ffff99"
            text "機嫌: [mood]" size 20 color "#99ffff"

    # --- 6. 見えないクリック判定ボタン ---
    # 頭部 (通常)
    button:
        xalign 0.5 ypos 60
        xsize 220 ysize 100
        background None
        action [
            SetVariable("total_clicks", total_clicks + 1),
            Function(add_effect, "star"),
            Function(play_random_voice, "mild"),
            SetVariable("persistent.intimacy", persistent.intimacy + 1),
            SetVariable("mood", mood - 1),
            Function(renpy.restart_interaction)
        ]

    # 耳 (特殊・敏感)
    button:
        xpos 570 ypos 130
        xsize 80 ysize 80
        background None
        action [
            SetVariable("total_clicks", total_clicks + 1),
            Function(add_effect, "special"),
            Function(play_random_voice, "sens"),
            SetVariable("persistent.intimacy", persistent.intimacy + 3),
            SetVariable("mood", mood - 5),
            Function(renpy.restart_interaction)
        ]

    # 胸部 (特殊・敏感)
    button:
        xalign 0.5 ypos 330
        xsize 250 ysize 180
        background None
        action [
            SetVariable("total_clicks", total_clicks + 1),
            Function(add_effect, "special"),
            Function(play_random_voice, "sens"),
            SetVariable("persistent.intimacy", persistent.intimacy + 8),
            SetVariable("mood", mood - 12),
            Function(renpy.restart_interaction)
        ]

    # 下腹部 (特殊・最高敏感)
    button:
        xalign 0.5 ypos 550
        xsize 220 ysize 150
        background None
        action [
            SetVariable("total_clicks", total_clicks + 1),
            Function(add_effect, "special"),
            Function(play_random_voice, "intense"),
            SetVariable("persistent.intimacy", persistent.intimacy + 15),
            SetVariable("mood", mood - 20),
            Function(renpy.restart_interaction)
        ]

    # 右下のアクションエリア
    hbox:
        xalign 0.98 yalign 0.98
        spacing 15
        textbutton "ショップへ":
            action Show("shop_screen")
            text_size 26
            text_color "#fff"
            text_hover_color "#ffcc00"

# --- ショップ画面 ---
screen shop_screen():
    modal True
    zorder 200
    add Solid("#000000aa")
    frame:
        xalign 0.5 yalign 0.4
        padding (30, 30)
        vbox:
            spacing 20
            text "購買部" size 40 color "#ffaa00" xalign 0.5
            text "現在の所持金: [persistent.money]円" size 24 xalign 0.5
            null height 20
            text "（アイテム入荷待ち……）" color "#888" xalign 0.5
            null height 30
            textbutton "戻る" action Hide("shop_screen") xalign 0.5:
                text_size 30
