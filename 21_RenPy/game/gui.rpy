# GUIの基本定義

# 文字の色
define gui.text_color = '#ffffff'
define gui.accent_color = '#ffc0cb'
define gui.idle_color = '#aaaaaa'
define gui.hover_color = '#ffffff'

# メインメニューなどの背景
image gui_background = "bg_classroom.png"

# フォントサイズ
define gui.text_size = 22
define gui.label_text_size = 24
define gui.button_text_size = 22

# ウィンドウの設定
define gui.textbox_height = 185
define gui.textbox_yalign = 1.0

# スタイル定義の補足
style default:
    font "font.ttf" # 日本語対応フォントに変更
    color gui.text_color
    size gui.text_size

style frame:
    background Solid("#00000088")
    padding (10, 10)

style bar:
    ysize 25
    left_bar Solid("#ffc0cb")
    right_bar Solid("#444")

# メインメニュー画面（エラー回避用）
screen main_menu():
    tag menu
    add "gui_background"
    vbox:
        xalign 0.5 yalign 0.5
        spacing 20
        text "[config.name]" size 40
        textbutton "スタート" action Start()
        textbutton "終了" action Quit()

# メッセージウィンドウ（会話用）
screen say(who, what):
    style_prefix "say"
    window:
        id "window"
        if who is not None:
            text who id "who"
        text what id "what"

style say_window:
    xalign 0.5 yalign 1.0
    xsize 1200 ysize 180
    background Solid("#000000aa")
    padding (20, 20)

style say_label:
    color "#ffc0cb"
    bold True

style say_dialogue:
    xpos 10 ypos 40

# ---- 終了確認ダイアログ（Ren'Py 8.5系 yesno_prompt 対策） ----

# Ren'Py が内部で呼び出す confirm スクリーンを上書き定義
screen confirm(message, yes_action, no_action):
    zorder 200
    modal True

    add Solid("#000000bb")

    frame:
        align (0.5, 0.5)
        padding (40, 30)
        background Solid("#222233cc")
        vbox:
            spacing 20
            xalign 0.5
            text message xalign 0.5 size 26 color "#ffffff"
            hbox:
                spacing 30
                xalign 0.5
                textbutton "はい" action yes_action
                textbutton "いいえ" action no_action

style confirm_button:
    background Solid("#ffc0cb88")
    padding (20, 10)

style confirm_button_text:
    color "#ffffff"
    size 24
    bold True
