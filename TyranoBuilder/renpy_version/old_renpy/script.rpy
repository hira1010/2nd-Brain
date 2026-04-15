# ヒロイン密着クリック＆チェキ経済ADV (製品版・安定動作モデル)

# --- キャラクター定義 ---
define h = Character(None) # ヒロイン（名前なし表示）

# --- 基本データの初期化 ---
# 親密度（永続保存）
default persistent.intimacy = 0
# 所持金（永続保存・初期値1000円）
default persistent.money = 1000
# ヒロインの機嫌
default mood = 100
# 親密度の目標値（ゲージの最大値）
default goal_intimacy = 1000
# 現在の親密度ランク
default intimacy_rank = 1
# デバッグ用のクリック回数（内部的に保持）
default total_clicks = 0

# 画面上のエフェクトを管理するリスト
default active_effects = []

# --- 画像の定義 (タグとファイルを紐付け) ---
image bg classroom_day = "images/bg classroom_day.png"
image heroine_rank1:
    "images/heroine_rank1.png"
    zoom 0.65 yalign 1.0
image heroine_rank2:
    "images/heroine_rank2.png"
    zoom 0.65 yalign 1.0
image heroine_rank3:
    "images/heroine_rank3.png"
    zoom 0.65 yalign 1.0
image effect_star = "images/effect_star.png"
image effect_heart = "images/effect_heart.png"

init python:
    import random
    import math

    # エフェクト（星やハート）の挙動を管理するクラス
    class ClickEffect:
        def __init__(self, x, y, etype="star"):
            self.x = x
            self.y = y
            self.etype = etype
            # 飛び散る角度と速度をランダムに決定
            angle = random.uniform(0, 6.28)
            speed = random.uniform(150, 450)
            self.dx = speed * math.cos(angle)
            self.dy = speed * math.sin(angle)
            # 回転を加える（製品版用の演出）
            self.rotation = random.uniform(0, 360)
            self.rot_speed = random.uniform(-180, 180)
            # 寿命（秒）
            self.life = 0.8
            self.max_life = 0.8
            
        def update(self, dt):
            # 位置と回転を更新
            self.x += self.dx * dt
            self.y += self.dy * dt
            self.rotation += self.rot_speed * dt
            # 寿命を減らす
            self.life -= dt
            return self.life > 0

    # スクリーンのタイマーから呼ばれる更新関数
    def update_effects():
        global active_effects
        if not active_effects:
            return
        
        new_list = []
        for e in active_effects:
            # 0.02秒（タイマーの間隔）分、状態を進める
            if e.update(0.02):
                new_list.append(e)
        active_effects = new_list
        # 画面を再描画してアニメーションを反映
        renpy.restart_interaction()

    # 音声をランダムに再生する関数（製品版用）
    def play_random_voice(category):
        # 指定されたカテゴリ（mild, sens, intense）からランダムに1〜3を選択
        voice_num = random.randint(1, 3)
        file_path = "audio/{}{}.wav".format(category, voice_num)
        # 音声を再生
        renpy.music.play(file_path, channel="sound", loop=False)

    # クリック時にエフェクトを追加する関数
    def add_effect(type="star"):
        global active_effects
        m_pos = renpy.get_mouse_pos()
        
        # タイプに応じて粒子の数と種類を切り替え
        if type == "special":
            count = 25 # スペシャルは大量に放出
            etype = "heart"
        elif type == "star":
            count = 6
            etype = "star"
        else: # heart
            count = 12
            etype = "heart"
            
        for _ in range(count):
            active_effects.append(ClickEffect(m_pos[0], m_pos[1], etype))

# --- ゲーム本編の流れ ---
label start:
    # 画面転換：教室の背景を表示
    scene bg classroom_day with fade
    
    # 導入メッセージ
    "（放課後の教室。彼女と二人きり……。）"
    "（指先で触れることで、彼女との距離を縮めることができるはずだ。）"
    
    # メインのやり取りループへ
    jump interaction_loop

label interaction_loop:
    # 変数リセット
    $ _return = None
    # インタラクション画面の呼び出し（ここでクリック待ちになる）
    call screen interaction
    
    # 特殊な戻り値（ランクアップなど）があれば対応
    if _return == "rank_up":
        jump rank_up_event
    
    # ループを繰り返す
    jump interaction_loop

# 親密度が上がった時のイベント
label rank_up_event:
    $ intimacy_rank += 1
    # 演出用の音声やメッセージをここに追加可能
    h "なんだか……君の視線が、前より熱い気がするよ。"
    "親密度ランクが [intimacy_rank] に上昇しました！"
    jump interaction_loop
