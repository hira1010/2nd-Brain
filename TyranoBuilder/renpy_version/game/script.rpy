# script.rpy - Ver 8.0 密着クリック＆チェキ経済版

# ==========================================
# 4. シナリオ進行 (Label)
# ==========================================

label start:
    # 怒り蓄積をリセットしてメイン画面へ
    $ p_anger = 0
    "「……ねえ、何見てるの？」"
    call screen main_interaction

# チェキ撮影イベント
label take_photo:
    # 売却価格計算
    $ base_price = 1000 * (p_rank ** 2)
    $ bonus = 1.5 if p_pleasure >= 100 else 1.0
    $ lens_bonus = 1.2 if has_lens else 1.0
    $ final_price = int(base_price * bonus * lens_bonus)

    # 演出
    scene white with flash
    # play sound "audio/shutter.mp3" # ※ファイルがない場合はスキップされます
    
    "チェキを撮影しました。"
    "現在のランク[p_rank]の価値：[final_price]円"
    
    # 報酬の追加とリセット
    $ p_money += final_price
    $ p_pleasure = 0 # 快感リセット
    $ p_anger = 0
    
    "「これは二人の協力活動（ビジネス）だからね」"
    jump start

# お仕置きタイム (連続クリックへの警告)
label punishment_start:
    hide screen main_interaction
    "「ちょっと……しつこすぎ。少し頭冷やして」"
    "（一定時間、操作が封印された！）"
    
    # 5秒間のポーズ
    $ renpy.pause(5.0)
    
    $ p_anger = 0
    "反省したようだ。"
    jump start

# ショップ画面
label open_shop:
    "ショップ店員「何を買う？」"
    menu:
        "リボン (1.5倍親密度) / 5000円" if not has_ribbon:
            if p_money >= 5000:
                $ p_money -= 5000
                $ has_ribbon = True
                "リボンを購入しました。親密度が上がりやすくなります！"
            else:
                "お金が足りないようだ……。"
                
        "香水 (2.0倍快感度) / 8000円" if not has_perfume:
            if p_money >= 8000:
                $ p_money -= 8000
                $ has_perfume = True
                "香水を購入しました。快感度が上がりやすくなります！"
            else:
                "お金が足りないようだ……。"
                
        "戻る":
            pass

    jump start
