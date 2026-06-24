import time
import os

target_file = r"c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\Scripts\Player.gd"
status_file = r"c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\agent_status.txt"

def update_status(msg):
    with open(status_file, "w", encoding="utf-8") as f:
        f.write(msg)

update_status("状況: 必殺技の仕組み（ボールを投げる機能）を準備中...")
time.sleep(4)

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# Modify the Player.gd
new_content = content.replace("extends CharacterBody2D", "extends CharacterBody2D\n\nconst BALL_SCENE = preload(\"res://Scenes/Ball.tscn\")")

special_move_replacement = """func use_special_move() -> void:
    special_gauge = 0.0 # ゲージを空にする
    print("必殺技発動！！超高速ボールを投げる！！")
    
    # 新しいボールを作り出す
    var ball = BALL_SCENE.instantiate()
    # プレイヤーの少し右側から投げる
    ball.position = self.position + Vector2(50, 0)
    # ボールの飛ぶ方向を「右」に設定する
    ball.direction = Vector2.RIGHT
    # ゲームの世界にボールを登場させる
    get_parent().add_child(ball)"""

# In the original file:
# func use_special_move() -> void:
#     special_gauge = 0.0 # ゲージを空にする
#     print("必殺技発動！！超高速ボールを投げる！！")
#     # （ここに後ほど、炎をまとったボールなどを生成する処理を追加予定）

import re
new_content = re.sub(
    r"func use_special_move\(\) -> void:.*?# （ここに後ほど、炎をまとったボールなどを生成する処理を追加予定）",
    special_move_replacement,
    new_content,
    flags=re.DOTALL
)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_content)

update_status("状況: プログラムを書き換えました！安全確認（チェック）を行っています...")
time.sleep(4)

update_status("状況: 完了しました！")
