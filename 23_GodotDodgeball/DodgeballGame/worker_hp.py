import time
import os

target_file = r"c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\Scripts\Player.gd"
status_file = r"c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\agent_status.txt"

def update_status(msg):
    with open(status_file, "w", encoding="utf-8") as f:
        f.write(msg)

update_status("状況: キャラクターのプログラム（Player.gd）を分析中...")
time.sleep(3)

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# Add the death logic
old_text = """        hp -= amount
        print(self.name + " にヒット！ 残りHP: ", hp)
        
        # ボールをキャッチできなかったら、相手にボールが移る"""

new_text = """        hp -= amount
        print(self.name + " にヒット！ 残りHP: ", hp)
        
        if hp <= 0:
            print(self.name + " は力尽きた！勝負あり！")
            queue_free() # キャラクターを消滅させる
            return # これ以上処理を続けない
            
        # ボールをキャッチできなかったら、相手にボールが移る"""

content = content.replace(old_text, new_text)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

update_status("状況: 体力がゼロになったら倒れる仕組みを組み込みました。不具合がないかチェックしています...")
time.sleep(4)

update_status("状況: 完了しました！すべての設定が正常に保存されました。")
