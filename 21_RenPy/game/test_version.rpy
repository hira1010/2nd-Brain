# ==========================================
# ヒロインクリッカー - 完全版スクリプト
# ==========================================

# ---- 1. 画像定義 ----

# 背景を画面サイズ(1280x720)にフィット表示
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

# ---- 3. 変数定義 ----

default p_intimacy  = 0.0    # 親密度
default p_pleasure  = 0.0    # 快感値
default p_rank      = 1      # ランク（1〜3）
default p_shake_type = None  # 演出の種類
default p_anger     = 0      # 怒りゲージ（連打防止）
default p_money     = 0      # 所持金

# アイテム所持フラグ
default has_vibrator  = False   # バイブ（快感2倍）
default has_super_vibe = False  # 強力バイブ（快感4倍）
default has_lotion    = False   # ローション（親密度1.5倍）
default has_aroma_oil = False   # 高級オイル（親密度3倍）
default has_camera    = False   # カメラ（写真売価1.5倍）

# ---- 4. Pythonロジック ----

init python:
    def click_action(part):
        """クリックされた部位に応じてステータスを更新する"""
        global p_intimacy, p_pleasure, p_rank, p_shake_type, p_anger

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
                p_pleasure += 5.0 * pleas_mult  # 股間はバイブ追加ボーナス
            p_shake_type = "shiver"

        # 1クリックで快感値が100を超えたら上限
        if p_pleasure > 100: p_pleasure = 100.0

        # ランクを更新
        if p_intimacy > 100: p_rank = 3
        elif p_intimacy > 40: p_rank = 2
        else: p_rank = 1

        # 怒りゲージを増加（連打するとお仕置き）
        p_anger += 1
        if p_anger > 20:
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
        align (0.05, 0.05)
        background Solid("#00000088")
        padding (15, 12)
        vbox:
            spacing 5
            text "★ Rank: [p_rank]"              size 28 color "#ff69b4" bold True
            text "💕 Love: [p_intimacy:.1f]"       color "#ffffff"  size 22
            text "🔥 Pleasure: [p_pleasure:.1f]"   color "#ff7799"  size 22
            text "💰 Money: [p_money]円"            color "#ffe066"  size 22

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
        "「……ねえ、何見てるの？」"
        "クリックしてヒロインと仲良くなろう！"
        "親密度が上がるとランクアップするよ。"
    call screen main_interaction
    return

# 撮影（チェキ）イベント
label take_photo:
    $ base_price = 1000 * (p_rank ** 2)
    $ bonus      = 1.5 if p_pleasure >= 70 else 1.0
    $ cam_bonus  = 1.5 if has_camera else 1.0
    $ final_price = int(base_price * bonus * cam_bonus)

    scene bg_classroom
    show heroine_main at bottom_center

    "パシャッ！"

    if p_rank == 3:
        "すごくいい写真が撮れた！ヒロインも満更でもなさそう。"
    elif p_rank == 2:
        "まあまあの写真。もっと仲良くなればいいのに。"
    else:
        "まだちょっと距離がある…もっとクリックしてみよう！"

    "写真の価値：[final_price]円"
    $ p_money  += final_price
    $ p_pleasure = 0.0
    $ p_anger    = 0

    jump start

# お仕置きイベント（連打しすぎると発生）
label punishment_start:
    hide screen main_interaction
    $ p_anger = 0
    "「ちょっと……しつこすぎ。少し頭冷やして」"
    "（ヒロインが怒り、一時的に操作が封印された！）"
    $ renpy.pause(5.0)
    "反省したようだ。"
    jump start

# ショップ
label open_shop:
    hide screen main_interaction
    "ショップ店員「何を買う？」"
    menu:
        "特製ローション (親密度1.5倍) / 3000円" if not has_lotion:
            if p_money >= 3000:
                $ p_money -= 3000
                $ has_lotion = True
                "ローションを購入しました。"
            else:
                "お金が足りないようだ……。"

        "低周波バイブ (快感2倍) / 5000円" if not has_vibrator:
            if p_money >= 5000:
                $ p_money -= 5000
                $ has_vibrator = True
                "バイブを購入しました。開発が捗りそうです。"
            else:
                "お金が足りないようだ……。"

        "高性能カメラ (写真売価1.5倍) / 10000円" if not has_camera:
            if p_money >= 10000:
                $ p_money -= 10000
                $ has_camera = True
                "カメラを購入しました。より良い写真が撮れます。"
            else:
                "お金が足りないようだ……。"

        "高級アロマオイル (親密度3.0倍) / 15000円" if not has_aroma_oil:
            if p_money >= 15000:
                $ p_money -= 15000
                $ has_aroma_oil = True
                "高級アロマオイルを購入しました！"
            else:
                "お金が足りないようだ……。"

        "強力電動マッサージ器 (快感4.0倍) / 20000円" if not has_super_vibe:
            if p_money >= 20000:
                $ p_money -= 20000
                $ has_super_vibe = True
                "強力マッサージ器を購入しました！"
            else:
                "お金が足りないようだ……。"

        "もどる":
            pass

    jump start
