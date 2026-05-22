# script.rpy - Ver 8.0 3エンジン統合版

init python:
    # --- 変数初期化 ---
    p_intimacy = 0.0
    p_pleasure = 0.0
    p_rank = 1
    p_money = 0
    p_anger = 0
    
    # アイテム所持フラグ
    has_vibrator = False
    has_super_vibe = False  # 強力バイブ
    has_lotion = False
    has_aroma_oil = False   # 高級オイル
    has_camera = False

    # --- 動的な立ち絵定義 ---
    # 快感度(p_pleasure)に応じて自動で表情を切り替える
    renpy.image("heroine_main", ConditionSwitch(
        "p_pleasure >= 70", "heroine_rank1_excited.png",
        "p_pleasure >= 30", "heroine_rank1_blush.png",
        "True", "heroine_rank1.png"
    ))

    # --- 部位設定 (位置, サイズ, 音声, 上昇量) ---
    PARTS_CONFIG = {
        "ear": {
            "pos": (550, 130), "size": (100, 100), "voice": "ear.mp3",
            "love_gain": 1.5, "pleas_gain": 0.0
        },
        "breast": {
            "pos": (500, 280), "size": (280, 180), "voice": "chest.mp3",
            "love_gain": 2.0, "pleas_gain": 5.0
        },
        "crotch": {
            "pos": (520, 580), "size": (220, 130), "voice": "crotch.mp3",
            "love_gain": 5.0, "pleas_gain": 10.0
        }
    }
    
    VOICE_DIR = "audio/"

    # --- クリック処理関数 ---
    def trigger_click_action(part_id):
        global p_intimacy, p_pleasure, p_anger, p_rank
        
        cfg = PARTS_CONFIG[part_id]
        
        # アイテムによるボーナス計算
        love_mult = 1.0
        if has_lotion: love_mult = 1.5
        if has_aroma_oil: love_mult = 3.0 # 高級オイルは3倍
        
        pleas_mult = 1.0
        if has_vibrator: pleas_mult = 2.0
        if has_super_vibe: pleas_mult = 4.0 # 強力バイブは4倍
        
        if part_id == "crotch" and (has_vibrator or has_super_vibe):
            pleas_mult *= 1.5 # 股間はさらに1.5倍効く
            
        # 数値加算
        p_intimacy += cfg["love_gain"] * love_mult
        p_pleasure += cfg["pleas_gain"] * pleas_mult
        p_anger += 1
        
        # ランクチェック
        if p_intimacy > 100: p_rank = 3
        elif p_intimacy > 40: p_rank = 2
        
        # 演出用に画面を再描画 (胸クリック時は揺らす)
        if part_id == "breast":
            renpy.show_screen("main_interaction", shake=True)
        else:
            renpy.restart_interaction()
            
        # 連続クリックしすぎるとお仕置きへ
        if p_anger > 20:
            renpy.jump("punishment_start")

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
        "特製ローション (親密度1.5倍) / 3000円" if not has_lotion:
            if p_money >= 3000:
                $ p_money -= 3000
                $ has_lotion = True
                "ローションを購入しました。ヒロインが少し感じやすくなったようです。"
            else:
                "お金が足りないようだ……。"
                
        "低周波バイブ (快感度アップ) / 5000円" if not has_vibrator:
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
                "カメラを購入しました。より良い写真が撮れそうです。"
            else:
                "お金が足りないようだ……。"
                
        "高級アロマオイル (親密度3.0倍) / 15000円" if not has_aroma_oil:
            if p_money >= 15000:
                $ p_money -= 15000
                $ has_aroma_oil = True
                "アロマオイルを購入しました。ヒロインの親愛度が爆発的に高まります。"
            else:
                "お金が足りないようだ……。"

        "強力電動マッサージ器 (快感4.0倍) / 20000円" if not has_super_vibe:
            if p_money >= 20000:
                $ p_money -= 20000
                $ has_super_vibe = True
                "強力なマッサージ器を購入しました。一発で絶頂まで持っていけそうです。"
            else:
                "お金が足りないようだ……。"

        "戻る":
            pass

    jump start
