
# -----------------------------------------------------
# Ren'Py Script - Interaction Debugging
# -----------------------------------------------------

# キャラクターの定義
define a = Character("広瀬 愛理", color="#e67e22")

# 画像の定義
image airi stage0 = "images/airi_neutral.png"
image airi stage1 = "images/airi_disheveled.png"
image airi stage2 = "images/airi_underwear.png"
image airi stage3 = "images/airi_bunny.png"

# インタラクティブ・スクリーン
screen interaction_screen():
    # キャラクター表示
    add "airi stage[airi_stage]" xalign 0.5 yalign 1.0

    # 判定ゾーンを「非常に分かりやすく」します
    # アルファ値を 0.5 (80) に上げて、はっきり見えるようにします
    # また、ボタンをクリックした時に音が鳴るようにします
    
    # 頭
    button:
        xpos 540 ypos 50 xsize 200 ysize 200
        action Return("head")
        background Solid("#ff000080") # はっきり見える赤
        hover_background Solid("#ff0000bb")
    
    # 胸
    button:
        xpos 540 ypos 280 xsize 200 ysize 150
        action Return("chest")
        background Solid("#00ff0080") # はっきり見える緑
        hover_background Solid("#00ff00bb")

    # 体
    button:
        xpos 490 ypos 450 xsize 300 ysize 250
        action Return("body")
        background Solid("#0000ff80") # はっきり見える青
        hover_background Solid("#0000ffbb")

# ゲーム開始
label start:
    $ airi_stage = 0
    $ touch_count = 0
    scene black
    
    # ダイアログがあるとインタラクションが開始されないため、
    # 最初に一つ空のメッセージを出して、クリック後に開始するか、
    # あるいはメッセージなしで開始します。
    
    "クリックしてインタラクションを開始します。"

    label interact_loop:
        # 画面を表示して入力を待つ
        call screen interaction_screen
        $ result = _return
        
        if result == "head":
            voice "audio/voice/head_01.ogg"
            a "えっ...！？ いきなり頭を撫でるなんて..."
        
        elif result == "chest":
            $ touch_count += 1
            if airi_stage == 0 and touch_count >= 3:
                $ airi_stage = 1
                $ touch_count = 0
                voice "audio/voice/chest_s0.ogg"
                a "あっ...！ 服が...。や、やだ、見ないでください...！"
            elif airi_stage == 1 and touch_count >= 3:
                $ airi_stage = 2
                $ touch_count = 0
                voice "audio/voice/chest_s1.ogg"
                a "もう...。こんな格好、愛理、どうなっちゃうの..."
            elif airi_stage == 2 and touch_count >= 3:
                $ airi_stage = 3
                $ touch_count = 0
                voice "audio/voice/chest_s2.ogg"
                a "は、恥ずかしい...。なんで私がバニーガールなんて...。"
            else:
                if airi_stage == 3:
                    voice "audio/voice/max_stage.ogg"
                    a "もう、これ以上脱ぐものなんてありませんよ...！"
                else:
                    voice "audio/voice/reject_01.ogg"
                    a "な、何をしてるんですか...！？ やめてください！"
        
        elif result == "body":
            voice "audio/voice/body_01.ogg"
            a "あぅ...。触らないでください..."
        
        jump interact_loop
