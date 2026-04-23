# Heroine Clicker - Main Script

# ---- 1. Image Definitions ----

# Background (1280x720)
image bg_classroom = im.Scale("bg_classroom.png", 1280, 720)

# ランク＋快感度に応じて立ち絵が自動で変わる
image heroine_main = ConditionSwitch(
    "p_rank == 3",                          "heroine_rank3.png",
    "p_rank == 2 and p_pleasure >= 70",     "heroine_rank2.png",
    "p_rank == 2",                          "heroine_rank2.png",
    "p_pleasure >= 70",                     "heroine_rank1_excited.png",
    "p_pleasure >= 30",                     "heroine_rank1_blush.png",
    "True",                                 "heroine_rank1.png",
)

# ハートエフェクト（PNG画像ではなく文字を使うことで四角くならない）
image heart_particle = Text("❤", size=80, color="#ff69b4")

# ---- 2. トランスフォーム（アニメーション）定義 ----

# キャラを画面中央下に固定配置（zoom で全身が画面に収まるよう縮小）
transform bottom_center:
    xalign 0.5
    yalign 1.0
    zoom 0.7

# ハートがふわっと上に浮かんで消えるアニメーション
transform heart_float(x, y):
    pos (x, y)
    anchor (0.5, 0.5)
    alpha 1.0
    zoom 0.15
    parallel:
        easeout 0.8 yoffset -150
    parallel:
        easeout 0.8 alpha 0.0
    parallel:
        linear 0.1 zoom 0.25
        linear 0.6 zoom 0.2

# 胸の揺れ演出（上下に揺れる）
transform breast_shake:
    xalign 0.5
    yalign 1.0
    zoom 0.7
    yoffset 0
    easein 0.05 yoffset 15
    easeout 0.05 yoffset 0
    easein 0.05 yoffset 10
    easeout 0.05 yoffset 0

# ビクッとする演出（左右に震える）
transform body_shiver:
    xalign 0.5
    yalign 1.0
    zoom 0.7
    xoffset 0
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 xoffset 0

# 画面フラッシュ演出
define flash = Fade(0.1, 0.0, 0.5, color="#fff")

# ---- 3. 変数定義 ----

# キャラクター定義
define l = Character("レミ", color="#ffc0cb")
define m = Character("結人", color="#87ceeb")

# ---- 3. 変数定義 ----

default p_intimacy  = 0.0    # 親密度
default p_pleasure  = 0.0    # 快感値
default p_rank      = 1      # ランク（1〜3）
default p_shake_type = None  # 演出の種類
default p_anger     = 0      # 怒りゲージ
default p_money     = 0      # 所持金

# アイテム所持フラグ
default has_vibrator  = False
default has_super_vibe = False
default has_lotion    = False
default has_aroma_oil = False
default has_camera    = False

# ---- 4. Pythonロジック ----

init python:
    def click_action(part):
        """クリックされた部位に応じてステータスを更新する"""
        global p_intimacy, p_pleasure, p_rank, p_shake_type, p_anger

        # 絶頂中などはクリック無効（必要なら）
        
        # クリックした場所にハートを表示
        m_pos = renpy.get_mouse_pos()
        renpy.show_screen("heart_layer", x=m_pos[0], y=m_pos[1])

        p_shake_type = None

        # アイテムボーナス計算
        love_mult = 1.0
        if has_aroma_oil:   love_mult = 3.0
        elif has_lotion:    love_mult = 1.5

        pleas_mult = 1.0
        if has_super_vibe:  pleas_mult = 4.0
        elif has_vibrator:  pleas_mult = 2.0

        # 部位ごとの処理
        if part == "ear":
            p_intimacy += 1.5 * love_mult
            p_shake_type = "shiver"
        elif part == "chest":
            p_intimacy += 2.0 * love_mult
            p_pleasure  += 5.0 * pleas_mult
            p_shake_type = "shake"
        elif part == "crotch":
            p_intimacy += 5.0 * love_mult
            p_pleasure  += 10.0 * pleas_mult
            if has_vibrator or has_super_vibe:
                p_pleasure += 5.0 * pleas_mult
            p_shake_type = "shiver"

        # 100に達したら絶頂イベントへ
        if p_pleasure >= 100:
            p_pleasure = 100.0
            renpy.jump("lemi_climax")
            return

        # ランクを更新
        if p_intimacy > 100: p_rank = 3
        elif p_intimacy > 40: p_rank = 2
        else: p_rank = 1

        # 怒りゲージ（連打防止）
        p_anger += 1
        if p_anger > 25:
            renpy.jump("punishment_start")
            return

        renpy.restart_interaction()

# ---- 5. スクリーン定義 ----

# ハートエフェクトのレイヤー（クリック位置に表示）
screen heart_layer(x, y):
    zorder 100
    add "heart_particle" at heart_float(x, y)
    timer 0.8 action Hide("heart_layer")

# メインのインタラクション画面
screen main_interaction():
    # 背景
    add "bg_classroom"

    # ヒロイン立ち絵（演出の種類によってアニメーション切り替え）
    if p_shake_type == "shake":
        add "heroine_main" at breast_shake
        timer 0.2 action SetVariable("p_shake_type", None)
    elif p_shake_type == "shiver":
        add "heroine_main" at body_shiver
        timer 0.2 action SetVariable("p_shake_type", None)
    else:
        add "heroine_main" at bottom_center

    # ステータス表示（左上）
    frame:
        align (0.02, 0.02)
        background Solid("#000000aa")
        padding (20, 15)
        xsize 300
        vbox:
            spacing 8
            text "Lemi" size 32 color "#ffc0cb" bold True font "font.ttf"
            
            # 親密度ゲージ
            vbox:
                spacing 2
                text "Love: [p_intimacy:.1f]" size 16 color "#ffffff"
                bar value p_intimacy range 100.0 xsize 260 ysize 15 left_bar Frame(Solid("#ff69b4")) right_bar Frame(Solid("#444444"))
            
            # 快感度ゲージ
            vbox:
                spacing 2
                text "Pleasure: [p_pleasure:.1f]" size 16 color "#ffffff"
                bar value p_pleasure range 100.0 xsize 260 ysize 15 left_bar Frame(Solid("#ff1493")) right_bar Frame(Solid("#444444"))

            text "Rank: [p_rank]" size 20 color "#ff69b4"
            text "Money: [p_money]円" size 18 color "#ffe066"

    # ---- 当たり判定ボタン（透明） ----
    imagebutton:
        idle  Solid("#00000000")
        hover Solid("#ffffff22")
        xysize (60, 60)
        pos (600, 180)
        action Function(click_action, "ear")

    imagebutton:
        idle  Solid("#00000000")
        hover Solid("#ffffff22")
        xysize (120, 80)
        pos (550, 320)
        action Function(click_action, "chest")

    imagebutton:
        idle  Solid("#00000000")
        hover Solid("#ffffff22")
        xysize (100, 100)
        pos (580, 600)
        action Function(click_action, "crotch")

    # ボタン群（右下）
    vbox:
        align (0.95, 0.92)
        spacing 8
        textbutton "📷 撮影" action Jump("take_photo")
        textbutton "🛒 ショップ" action Jump("open_shop")

# ---- 6. ゲーム進行ラベル ----

label start:
    $ p_anger = 0
    scene bg_classroom
    if p_intimacy == 0.0:
        l "「……あんた、さっきから何見てるわけ？」"
        l "「……別に減るもんじゃないし。好きにすれば」"
        "（クリックしてレミと仲良くなろう。親密度が上がると反応が変わるよ。）"
    call screen main_interaction
    return

# 絶頂イベント
label lemi_climax:
    hide screen main_interaction
    scene bg_classroom
    show heroine_main at body_shiver
    with flash # 画面フラッシュ
    
    l "「あ、く……っ！？ ちょっと、今のは……っ！！」"
    
    "（レミは激しい快感に震えている……！）"
    
    $ p_intimacy += 10.0
    $ p_pleasure = 0.0
    $ p_anger = 0
    
    l "「……はぁ、はぁ……。あんた、後で覚えてなさいよ……」"
    
    "（親密度が10増加した。）"
    
    jump start

# 撮影（チェキ）イベント
label take_photo:
    $ base_price = 1000 * (p_rank ** 2)
    $ bonus      = 1.5 if p_pleasure >= 70 else 1.0
    $ cam_bonus  = 1.5 if has_camera else 1.0
    $ final_price = int(base_price * bonus * cam_bonus)

    scene bg_classroom
    show heroine_main at bottom_center

    "（パシャッ！）"

    if p_rank == 3:
        l "「……別に、あんたになら撮られてもいいけど。変なところには出さないでよね」"
        "レミは少し照れながらも、カメラに視線をくれた。"
    elif p_rank == 2:
        l "「……また撮るの？ 好きね、あんたも」"
        "レミは呆れつつも、拒む様子はない。"
    else:
        l "「……何？ 記録でも取ってるわけ。趣味悪いわね」"
        "まだ冷たい視線を感じる。もっと距離を縮める必要がありそうだ。"

    "写真の価値：[final_price]円"
    $ p_money  += final_price
    $ p_pleasure = 0.0
    $ p_anger    = 0

    jump start

# お仕置きイベント
label punishment_start:
    hide screen main_interaction
    $ p_anger = 0
    l "「……いい加減にして。さっきからしつこすぎるわよ」"
    l "「少し頭冷やしなさい。……顔、近すぎ」"
    "（レミを怒らせてしまった！ しばらく操作できない……）"
    $ renpy.pause(5.0)
    "レミの機嫌が少し直ったようだ。"
    jump start

# ショップ
label open_shop:
    hide screen main_interaction
    l "「……何が欲しいの？（所持金：[p_money]円）」"
    l "「私の許可なく、変なもの持ち込まないでよ」"
    menu:
        "特製ローション (Love x1.5) / 3000円" if not has_lotion:
            if p_money >= 3000:
                $ p_money -= 3000
                $ has_lotion = True
                "ローションを購入した。肌になじみやすそうだ。"
            else:
                "お金が足りない。レミに冷ややかな目で見られた……。"

        "低周波バイブ (Pleasure x2.0) / 5000円" if not has_vibrator:
            if p_money >= 5000:
                $ p_money -= 5000
                $ has_vibrator = True
                "バイブを購入した。反応を見るのが楽しみだ。"
            else:
                "お金が足りない。"

        "高品質カメラ (Money x1.5) / 10000円" if not has_camera:
            if p_money >= 10000:
                $ p_money -= 10000
                $ has_camera = True
                "カメラを購入した。より細部まで鮮明に映るだろう。"
            else:
                "お金が足りない。"

        "高級アロマオイル (Love x3.0) / 15000円" if not has_aroma_oil:
            if p_money >= 15000:
                $ p_money -= 15000
                $ has_aroma_oil = True
                "高級アロマを購入した。良い香りが漂う……。"
            else:
                "お金が足りない。"

        "強力電動マッサージ器 (Pleasure x4.0) / 20000円" if not has_super_vibe:
            if p_money >= 20000:
                $ p_money -= 20000
                $ has_super_vibe = True
                "強力マッサージ器を購入した。かなりの威力がありそうだ。"
            else:
                "お金が足りない。"

        "戻る":
            pass

    jump start
