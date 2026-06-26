import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(120, 160, title="Pyxel Racing")
        
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        # 自機の初期位置
        self.player_x = 54
        self.player_y = 130
        self.player_w = 12
        self.player_h = 16
        self.player_speed = 2.5
        
        # はみ出し防止の壁 (画面幅120)
        self.left_wall = 20
        self.right_wall = 100
        
        # 敵車リスト [{x, y, w, h, speed, color}, ...]
        self.enemies = []
        
        # 背景（道路の白線）
        self.lines = [0, 40, 80, 120]
        
        self.score = 0
        self.is_gameover = False

    def update(self):
        if self.is_gameover:
            if pyxel.btnp(pyxel.KEY_R): # リトライ
                self.reset()
            return
            
        # プレイヤー移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= self.player_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += self.player_speed
            
        # 画面端の制限
        self.player_x = max(self.left_wall, min(self.player_x, self.right_wall - self.player_w))
        
        # スコア加算
        self.score += 1
        
        # 背景のスクロール
        for i in range(len(self.lines)):
            self.lines[i] += 2
            if self.lines[i] > 160:
                self.lines[i] -= 160
                
        # 敵の生成（スコアに応じて頻度が増える）
        spawn_rate = max(15, 60 - self.score // 50)
        if pyxel.frame_count % spawn_rate == 0:
            ex = random.randint(self.left_wall, self.right_wall - int(self.player_w))
            speed = random.uniform(1.5, 3.5)
            color = random.choice([8, 9, 10, 14]) # 様々な車の色(赤、オレンジ、黄、ピンク)
            self.enemies.append({"x": ex, "y": -20, "w": 12, "h": 16, "speed": speed, "color": color})
            
        # 敵の移動と当たり判定
        for e in self.enemies[:]:
            e["y"] += e["speed"]
            
            # 当たり判定 (シンプルな矩形判定)
            if (self.player_x < e["x"] + e["w"] and 
                self.player_x + self.player_w > e["x"] and 
                self.player_y < e["y"] + e["h"] and 
                self.player_y + self.player_h > e["y"]):
                self.is_gameover = True
                
            # 画面外に出た敵を削除
            if e["y"] > 160:
                self.enemies.remove(e)

    def draw(self):
        pyxel.cls(0) # 背景黒
        
        # コースの描画（芝生と道路）
        pyxel.rect(0, 0, self.left_wall, 160, 3) # 左の緑
        pyxel.rect(self.right_wall, 0, 120 - self.right_wall, 160, 3) # 右の緑
        pyxel.rect(self.left_wall, 0, self.right_wall - self.left_wall, 160, 1) # 道路（暗いグレー）
        
        # 道路の中央の白線
        for y in self.lines:
            pyxel.rect(59, y, 2, 20, 7)
            
        if self.is_gameover:
            # ゲームオーバー画面
            pyxel.rect(10, 60, 100, 40, 0)
            pyxel.rectb(10, 60, 100, 40, 8)
            pyxel.text(42, 65, "GAME OVER", 8)
            pyxel.text(35, 75, f"SCORE: {self.score}", 7)
            pyxel.text(35, 88, "- PRESS R -", 13)
            return

        # 敵の描画
        for e in self.enemies:
            ex, ey = int(e["x"]), int(e["y"])
            ew, eh = int(e["w"]), int(e["h"])
            # 敵の車本体
            pyxel.rect(ex, ey, ew, eh, e["color"])
            # タイヤ
            pyxel.rect(ex-1, ey+2, 1, 4, 0)
            pyxel.rect(ex+ew, ey+2, 1, 4, 0)
            pyxel.rect(ex-1, ey+10, 1, 4, 0)
            pyxel.rect(ex+ew, ey+10, 1, 4, 0)
            
        # プレイヤーの描画
        px, py = int(self.player_x), int(self.player_y)
        pw, ph = int(self.player_w), int(self.player_h)
        pyxel.rect(px, py, pw, ph, 11) # 青系の車
        pyxel.rect(px-1, py+2, 1, 4, 0)
        pyxel.rect(px+pw, py+2, 1, 4, 0)
        pyxel.rect(px-1, py+10, 1, 4, 0)
        pyxel.rect(px+pw, py+10, 1, 4, 0)
        
        # スコア描画
        pyxel.text(2, 2, f"SCORE: {self.score}", 7)

if __name__ == '__main__':
    App()
