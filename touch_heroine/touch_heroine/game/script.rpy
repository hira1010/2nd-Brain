# 画像なしで最低限動くテスト版

init python:
    def click_action(part):
        global p_intimacy, p_pleasure, p_rank, p_shake_type
        p_shake_type = None

        if part == "ear":
            p_intimacy += 1.5
            p_shake_type = "shiver"
        elif part == "chest":
            p_intimacy += 2.0
            p_pleasure += 5.0
            p_shake_type = "shake"
        elif part == "crotch":
            p_intimacy += 5.0
            p_pleasure += 10.0
            p_shake_type = "shiver"

        if p_intimacy > 100:
            p_rank = 3
        elif p_intimacy > 40:
            p_rank = 2
        else:
            p_rank = 1

        renpy.restart_interaction()

default p_intimacy = 0.0
default p_pleasure = 0.0
default p_rank = 1
default p_shake_type = None

transform bottom_center:
    xalign 0.5 yalign 1.0

transform breast_shake:
    xalign 0.5 yalign 1.0
    easein 0.05 yoffset 15 easeout 0.05 yoffset 0 easein 0.05 yoffset 10 easeout 0.05 yoffset 0

transform body_shiver:
    xalign 0.5 yalign 1.0
    linear 0.05 xoffset 5 linear 0.05 xoffset -5 linear 0.05 xoffset 0

screen main_interaction():
    # 背景（画像なしでも黒で表示）
    add Solid("#1a1a2e")

    # 仮の立ち絵（ピンクの四角で代用）
    if p_shake_type == "shake":
        add Solid("#ff69b4", xysize=(400, 600)) at breast_shake
        timer 0.25 action SetVariable("p_shake_type", None)
    elif p_shake_type == "shiver":
        add Solid("#ff69b4", xysize=(400, 600)) at body_shiver
        timer 0.25 action SetVariable("p_shake_type", None)
    else:
        add Solid("#ff69b4", xysize=(400, 600)) at bottom_center

    # ステータス
    frame:
        align (0.05, 0.05)
        background Solid("#00000077")
        padding (15, 15)
        vbox:
            text "Rank: [p_rank]" size 40 color "#ff69b4" bold True
            text "Love: [p_intimacy:.1f]" color "#ffffff" size 30
            text "Pleasure: [p_pleasure:.1f]" color "#ff1493" size 30

    # クリック判定
    imagebutton:
        idle Solid("#00000000") hover Solid("#ffffff33")
        xysize (80, 80) pos (520, 180) action Function(click_action, "ear")
    imagebutton:
        idle Solid("#00000000") hover Solid("#ffffff33")
        xysize (160, 120) pos (480, 320) action Function(click_action, "chest")
    imagebutton:
        idle Solid("#00000000") hover Solid("#ffffff33")
        xysize (120, 140) pos (540, 550) action Function(click_action, "crotch")

    textbutton "撮影" action Jump("take_photo") align (0.95, 0.9)

label start:
    scene black
    "テスト版を開始します。ピンクの四角がヒロインです。"
    call screen main_interaction
    return

label take_photo:
    "撮影はまだ未実装です。"
    return