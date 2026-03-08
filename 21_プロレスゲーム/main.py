import pyxel
import math

# 定数
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
RING_MIN_Y = 50
RING_MAX_Y = 110
RING_MIN_X = 10
RING_MAX_X = 150

class Wrestler:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.color = color
        self.name = name
        self.hp = 100
        self.direction = 1 # 1: 右, -1: 左
        self.state = "IDLE"
        self.state_frame = 0

    def update(self):
        self.state_frame += 1
        # 基本のアニメーション（仮）
        pass

    def draw(self):
        # 影
        pyxel.ellib(self.x + 2, self.y + self.h - 2, 12, 4, 0)
        # 本体 (仮の矩形描画)
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)
        # 向きを示すドット
        eye_x = self.x + (12 if self.direction == 1 else 2)
        pyxel.pset(eye_x, self.y + 4, 7)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pro-Wrestling Game Alpha")
        self.p1 = Wrestler(40, 80, 12, "PLAYER 1")
        self.p2 = Wrestler(100, 80, 8, "PLAYER 2")
        pyxel.run(self.update, self.draw)

    def update(self):
        # P1 移動操作 (仮)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.p1.x -= 2
            self.p1.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.p1.x += 2
            self.p1.direction = 1
        if pyxel.btn(pyxel.KEY_UP):
            self.p1.y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.p1.y += 1

        # 画面外制限
        self.p1.x = max(RING_MIN_X, min(RING_MAX_X - self.p1.w, self.p1.x))
        self.p1.y = max(RING_MIN_Y, min(RING_MAX_Y - self.p1.h, self.p1.y))

    def draw(self):
        pyxel.cls(13) # 背景色：グレー（会場）
        
        # リングの描画
        pyxel.rect(RING_MIN_X, RING_MIN_Y, RING_MAX_X - RING_MIN_X, RING_MAX_Y - RING_MIN_Y, 7) # マット：白
        pyxel.rectb(RING_MIN_X, RING_MIN_Y, RING_MAX_X - RING_MIN_X, RING_MAX_Y - RING_MIN_Y, 1) # 縁：青
        
        # キャラクター描画
        # 重なり順を考慮
        wrestlers = [self.p1, self.p2]
        wrestlers.sort(key=lambda w: w.y)
        for w in wrestlers:
            w.draw()

        # UI
        pyxel.text(5, 5, f"{self.p1.name}: {self.p1.hp}", 7)
        pyxel.text(100, 5, f"{self.p2.name}: {self.p2.hp}", 7)

if __name__ == "__main__":
    App()
