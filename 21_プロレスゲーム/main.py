import pyxel
import math

# 定数
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
RING_X_MIN = 20
RING_X_MAX = 140
RING_Y_MIN = 50 # 観客席のために少し下げる
RING_Y_MAX = 110

class Particle:
    def __init__(self, x, y, color, kind="SPARK"):
        self.x = x
        self.y = y
        self.vx = pyxel.rndf(-2, 2)
        self.vy = pyxel.rndf(-2, 2)
        self.life = 10
        self.color = color
        self.kind = kind

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.kind == "SPARK":
            pyxel.pset(self.x, self.y, self.color)
        else:
            pyxel.circ(self.x, self.y, 1, self.color)


class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.color = color
        self.hp = 100
        self.max_hp = 100
        self.gauge = 0
        self.max_gauge = 100
        self.direction = 1 # 1: right, -1: left
        self.state = "IDLE" # IDLE, WALK, STRIKE, GRAPPLE, SPECIAL, HURT, DOWN, PINNED, WIN
        self.state_frame = 0
        self.anim_frame = 0
        self.dash_timer = 0
        self.is_dashing = False


    def update_animation(self):
        self.state_frame += 1
        if pyxel.frame_count % 5 == 0:
            self.anim_frame += 1

    def draw(self):
        # 影
        if self.state != "SPECIAL":
            pyxel.ellib(self.x + 2, self.y + self.h - 2, 12, 4, 0)
        
        # イメージバンク 0 から描画
        u = 0
        if self.state == "IDLE":
            u = (self.anim_frame % 2) * 16
        elif self.state == "WALK":
            u = 32 + (self.anim_frame % 2) * 16
        elif self.state == "STRIKE":
            u = 64 + (min(self.state_frame // 3, 1)) * 16
        elif self.state == "GRAPPLE":
            u = 128
        elif self.state == "SPECIAL":
            u = 144 # バストラ用
        elif self.state == "HURT":
            u = 96
        elif self.state == "DOWN" or self.state == "PINNED":
            u = 112
        elif self.state == "WIN":
            u = 144

        v = 0 if self.color == 12 else 16
        pyxel.blt(self.x, self.y, 0, u, v, self.w * self.direction, self.h, 0)

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 12)
        self.attack_cooldown = 0

    def update(self, opponent):
        if self.state in ["HURT", "DOWN", "PINNED", "WIN", "SPECIAL"]:
            if self.state == "HURT" and self.state_frame > 15: self.state = "IDLE"
            if self.state == "DOWN" and self.state_frame > 60 and self.hp > 0: self.state = "IDLE"
            if self.state == "SPECIAL" and self.state_frame > 40: self.state = "IDLE"
            self.update_animation()
            return

        # ダッシュ入力 (ダブルタップ判定)
        if self.state != "SPECIAL":
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                if self.dash_timer > 0:
                    self.is_dashing = True
                self.dash_timer = 15
        
        if self.dash_timer > 0:
            self.dash_timer -= 1
        
        # 移動
        move_x, move_y = 0, 0
        if self.state not in ["STRIKE", "GRAPPLE", "SPECIAL"]:
            speed = 3.5 if self.is_dashing else 2.0
            if pyxel.btn(pyxel.KEY_LEFT):
                move_x, self.direction = -speed, -1
            elif pyxel.btn(pyxel.KEY_RIGHT):
                move_x, self.direction = speed, 1
            
            y_speed = 2.0 if self.is_dashing else 1.5
            if pyxel.btn(pyxel.KEY_UP): move_y = -y_speed
            elif pyxel.btn(pyxel.KEY_DOWN): move_y = y_speed

            if move_x == 0 and move_y == 0:
                self.is_dashing = False

            self.x += move_x
            self.y += move_y
            self.x = max(RING_X_MIN, min(RING_X_MAX - self.w, self.x))
            self.y = max(RING_Y_MIN, min(RING_Y_MAX - self.h, self.y))

            if move_x != 0 or move_y != 0: 
                self.state = "WALK"
                if self.is_dashing and pyxel.frame_count % 3 == 0:
                    # ダッシュの煙エフェクト
                    app.particles.append(Particle(self.x + 8, self.y + 14, 13, "DUST"))
            else: 
                self.state = "IDLE"

        # 攻撃(Z: 打撃, X: 投げ, Space: 必殺)
        if self.attack_cooldown <= 0:
            if pyxel.btnp(pyxel.KEY_Z):
                if self.is_dashing:
                    self.state, self.state_frame, self.attack_cooldown = "STRIKE", 0, 25
                    # ダッシュ攻撃（威力高め・リーチ長め想定）
                else:
                    self.state, self.state_frame, self.attack_cooldown = "STRIKE", 0, 15
            elif pyxel.btnp(pyxel.KEY_X):
                self.state, self.state_frame, self.attack_cooldown = "GRAPPLE", 0, 30
            elif pyxel.btnp(pyxel.KEY_SPACE) and self.gauge >= self.max_gauge:
                self.state, self.state_frame, self.attack_cooldown = "SPECIAL", 0, 60
                self.gauge = 0

        if self.state in ["STRIKE", "GRAPPLE"] and self.state_frame > 12:
            self.state = "IDLE"

        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        self.update_animation()


class CPU(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 8)

    def update(self, player):
        if self.state in ["HURT", "DOWN", "PINNED", "WIN"]:
             if self.state == "HURT" and self.state_frame > 15: self.state = "IDLE"
             if self.state == "DOWN" and self.state_frame > 90 and self.hp > 0: self.state = "IDLE"
             self.update_animation()
             return

        # AI
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        # 状態リセット
        if self.state == "WALK": self.state = "IDLE"

        # ターゲットとの軸合わせ
        if self.state == "IDLE":
            # Y軸合わせ
            if abs(dy) > 4:
                self.y += 1.2 if dy > 0 else -1.2
                self.state = "WALK"
            
            # 距離調整
            if dist > 30: # 遠い：近づく
                self.x += 1.0 if dx > 0 else -1.0
                self.direction = 1 if dx > 0 else -1
                self.state = "WALK"
            elif dist < 12: # 近すぎ：少し離れる
                self.x -= 0.8 if dx > 0 else -0.8
                self.state = "WALK"
            else: # 適切な間合い：攻撃か待機
                if pyxel.frame_count % 20 == 0:
                    r = pyxel.rndf(0, 1)
                    if r < 0.6:
                        self.state, self.state_frame = "STRIKE", 0
                    elif r < 0.9:
                        self.state, self.state_frame = "GRAPPLE", 0
                    else:
                        # 挑発（仮：IDLEで待機）
                        pass

        if self.state in ["STRIKE", "GRAPPLE"] and self.state_frame > 12:
            self.state = "IDLE"


        self.x = max(RING_X_MIN, min(RING_X_MAX - self.w, self.x))
        self.y = max(RING_Y_MIN, min(RING_Y_MAX - self.h, self.y))
        self.update_animation()

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pro-Wrestling Ultimate 2D")
        self.init_assets()
        self.player = Player(40, 80)
        self.enemy = CPU(100, 80)
        self.pin_count = 0
        self.pin_timer = 0
        self.game_over = False
        self.crowd_offset = 0
        self.hit_stop = 0
        self.particles = []
        global app
        app = self
        pyxel.run(self.update, self.draw)


    def init_assets(self):
        # 詳細なドット絵セット (Player) - 既存コードから流用・強化
        pyxel.image(0).set(0, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0000051111500000", "000055FFFF550000", "0005FFF77FFF5000", "0057777777777500", "0057775115777500", "0057751111577500", "0005511111155000", "0000511111150000", "0000511111150000", "0000577007750000", "0000577007750000", "0000555005550000"])
        pyxel.image(0).set(16, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0000051111500000", "000055FFFF550000", "005FFFF77FFFF500", "0577777777777750", "0577775115777750", "0577751111577750", "0005511111155000", "0000511111150000", "0000511111150000", "0000577007750000", "0000577007750000", "0000555005550000"])
        pyxel.image(0).set(64, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0000051111500000", "000055FFFF550000", "0005FFFF77750000", "0057777777750000", "0577775115550000", "0577751111500000", "0005511111155000", "0000511111150000", "0000511111150000", "0000577007750000", "0000577007750000", "0000555005550000"])
        pyxel.image(0).set(80, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0000051111500000", "000055FFFF550000", "000005FFFF777777", "000005777777777A", "000005777511155A", "0000057751111500", "0005511111155000", "0000511111150000", "0000511111150000", "0000577007750000", "0000577007750000", "0000555005550000"])
        pyxel.image(0).set(96, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0000051111500000", "00055FFFF5500000", "005FFFFFF5500000", "0577777777500000", "0577711115500000", "0055111150000000", "0005111150000000", "0005111150000000", "0005770775000000", "0005770775000000", "0005550555000000", "0000000000000000"])
        pyxel.image(0).set(112, 0, ["0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000", "0000001FF1100000", "055551F11F155550", "05FFFF11111FFFF5", "0577777777777775", "0055511111111550", "0000511111111500", "0000577555577500", "0000577500577500", "0000555500555500", "0000000000000000"])
        pyxel.image(0).set(128, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0000051111500000", "00055FFFF5500000", "005FFFFFF5500000", "0577777777500000", "0577711115500000", "0055111150000000", "0005111150000000", "0005111150000000", "0005770775000000", "0005770775000000", "0005550555000000", "0000000000000000"])
        pyxel.image(0).set(144, 0, ["0000055555500000", "0000511FF1150000", "000051F11F150000", "0000511111150000", "0001051111501000", "001715FFFF517100", "0017777777777100", "0017777777777100", "0005777777775000", "0005111111115000", "0005111111115000", "0005111111115000", "0005777007775000", "0005777007775000", "0005555005555000", "0000000000000000"])
        
        # Walk アニメーション (pset によるコピー)
        for i in range(16):
            for j in range(16):
                pyxel.image(0).pset(32+i, j, pyxel.image(0).pget(i, j))
                pyxel.image(0).pset(48+i, j, pyxel.image(0).pget(16+i, j))

        # Enemy パレット変換
        for i in range(160):
            for j in range(16):
                c = pyxel.image(0).pget(i, j)
                pyxel.image(0).pset(i, j+16, (8 if c==12 else (13 if c==7 else c)))

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R): self.__init__()
            return

        if self.hit_stop > 0:
            self.hit_stop -= 1
            return

        # パーティクル更新
        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)


        self.crowd_offset = (pyxel.frame_count // 10) % 2
        
        self.player.update(self.enemy)
        self.enemy.update(self.player)

        # 打撃ヒット
        if self.player.state == "STRIKE" and self.player.state_frame == 5:
            if abs(self.player.y - self.enemy.y) < 8 and abs((self.player.x + 8 * self.player.direction) - self.enemy.x) < 14:
                self.enemy.hp -= 8 if not self.player.is_dashing else 12
                self.player.gauge = min(self.player.max_gauge, self.player.gauge + 10)
                self.enemy.state, self.enemy.state_frame = "HURT", 0
                self.hit_stop = 5
                for _ in range(5):
                    self.particles.append(Particle(self.enemy.x + 8, self.enemy.y + 8, 7 if pyxel.frame_count % 2 == 0 else 10))
                if self.enemy.hp <= 0: self.enemy.state = "DOWN"


        # 投げヒット
        if self.player.state == "GRAPPLE" and self.player.state_frame == 5:
            if abs(self.player.y - self.enemy.y) < 6 and abs(self.player.x - self.enemy.x) < 10:
                self.enemy.hp -= 20
                self.player.gauge = min(self.player.max_gauge, self.player.gauge + 15)
                self.enemy.state, self.enemy.state_frame = "DOWN", 0
                self.enemy.x += 24 * self.player.direction
                self.hit_stop = 8
                for _ in range(8):
                    self.particles.append(Particle(self.enemy.x + 8, self.enemy.y + 8, 14, "DUST"))


        # 必殺技 (バックドロップ風)
        if self.player.state == "SPECIAL":
            if self.player.state_frame < 5:
                self.enemy.x, self.enemy.y = self.player.x - 4*self.player.direction, self.player.y
            elif self.player.state_frame < 30:
                # 持ち上げ
                self.enemy.x = self.player.x - 2*self.player.direction
                self.enemy.y = self.player.y - 12
                self.player.y -= 0.5 if self.player.state_frame <15 else -0.5
                # ヒットストップ中でもここを飛ばさないように App.update で制御されている
            elif self.player.state_frame == 30:
                # 叩きつけ
                self.enemy.hp -= 45
                self.enemy.state, self.enemy.state_frame = "DOWN", 0
                self.enemy.y = self.player.y + 4
                self.enemy.x -= 10 * self.player.direction
                self.hit_stop = 15
                # pyxel.play(0, 0) # 仮のSE
                for _ in range(15):
                    self.particles.append(Particle(self.enemy.x + 8, self.enemy.y + 8, 7))



        # フォール(自動開始)
        if self.enemy.state == "DOWN" and abs(self.player.x - self.enemy.x) < 12 and abs(self.player.y - self.enemy.y) < 8:
            self.enemy.state = "PINNED"
            self.player.state = "PINNED"
            self.pin_count = 0
            self.pin_timer = 30 # 最初のカウントを早めるための初期値
        
        if self.enemy.state == "PINNED":
            self.pin_timer += 1
            if self.pin_timer % 45 == 0: # 約1.5秒間隔
                self.pin_count += 1
                if self.pin_count >= 3:
                    self.game_over = True
                    self.player.state = "WIN"
            
            # キックアウト (HPが多いほど抜けやすいが、判定頻度を落とす)
            if self.enemy.hp > 0 and self.pin_timer % 30 == 0:
                if pyxel.rndf(0, 1) < (self.enemy.hp / 250): # 確率を調整
                    self.enemy.state, self.player.state = "IDLE", "IDLE"

    def draw(self):
        pyxel.cls(1) # 背景色
        
        # 観客席 (Crowd)
        for i in range(0, SCREEN_WIDTH, 8):
            color = 13 if (i // 8) % 2 == self.crowd_offset else 5
            pyxel.rect(i, 10, 6, 12, color)
            pyxel.rect(i+2, 8, 2, 2, 14) # Head

        # リング外
        pyxel.rect(0, 25, SCREEN_WIDTH, SCREEN_HEIGHT-25, 4)

        # リング (Mat)
        pyxel.rect(RING_X_MIN, RING_Y_MIN, RING_X_MAX - RING_X_MIN, RING_Y_MAX - RING_Y_MIN, 7)
        
        # 支柱 (Posts)
        for px, py in [(RING_X_MIN, RING_Y_MIN), (RING_X_MAX, RING_Y_MIN), (RING_X_MIN, RING_Y_MAX), (RING_X_MAX, RING_Y_MAX)]:
            pyxel.rect(px-2, py-15, 4, 20, 13)

        # 3段ロープ (Ropes)
        for h in [5, 10, 15]:
            # 奥
            pyxel.line(RING_X_MIN, RING_Y_MIN-h, RING_X_MAX, RING_Y_MIN-h, 12)
            # 手前
            pyxel.line(RING_X_MIN, RING_Y_MAX-h, RING_X_MAX, RING_Y_MAX-h, 12)
            # 左右
            pyxel.line(RING_X_MIN, RING_Y_MIN-h, RING_X_MIN, RING_Y_MAX-h, 12)
            pyxel.line(RING_X_MAX, RING_Y_MIN-h, RING_X_MAX, RING_Y_MAX-h, 12)

        # エンティティ描画
        ents = [self.player, self.enemy]
        ents.sort(key=lambda e: e.y)
        for e in ents: e.draw()

        # パーティクル描画
        for p in self.particles: p.draw()


        # UI
        # HP Bars
        pyxel.rect(5, 5, 52, 4, 0)
        pyxel.rect(6, 6, self.player.hp // 2, 2, 11)
        pyxel.rect(103, 5, 52, 4, 0)
        pyxel.rect(104, 6, self.enemy.hp // 2, 2, 8)
        
        # Special Gauge
        pyxel.rect(5, 110, 52, 3, 0)
        pyxel.rect(6, 111, self.player.gauge // 2, 1, 10 if self.player.gauge < 100 else 9)
        if self.player.gauge >= 100:
            pyxel.text(5, 114, "SPECIAL READY!", (pyxel.frame_count // 5) % 16)

        # Pin Count Display (Large Center)
        if self.enemy.state == "PINNED":
            c = self.pin_count
            if c > 0:
                pyxel.text(78, 40, str(c), 10)
                # カウントごとにフラッシュ
                if self.pin_timer % 45 < 10:
                    pyxel.rectb(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 7)

        if self.game_over:
            pyxel.rect(30, 50, 100, 30, 0)
            pyxel.text(55, 58, "WINNER: PLAYER", 11)
            pyxel.text(45, 70, "PRESS R TO RESTART", 7)

if __name__ == "__main__":
    App()
