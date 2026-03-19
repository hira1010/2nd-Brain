import pyxel
import math

# 定数
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
FLOOR_MIN_Y = 60
FLOOR_MAX_Y = 110

class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.color = color
        self.hp = 100
        self.max_hp = 100
        self.direction = 1 # 1: right, -1: left
        self.state = "IDLE" # IDLE, WALK, ATTACK, HURT, DIE
        self.state_frame = 0
        self.anim_frame = 0

    def update_animation(self):
        self.state_frame += 1
        # アニメーション速度の調整
        if pyxel.frame_count % 5 == 0:
            self.anim_frame += 1

    def draw(self):
        # 影 (透明度を意識した半透明擬似)
        pyxel.ellib(self.x + 2, self.y + self.h - 2, 12, 4, 0)
        
        # キャラクター描画 (image 0)
        # 状態に応じた u 座標の決定
        u = 0
        if self.state == "IDLE":
            u = (self.anim_frame % 2) * 16
        elif self.state == "WALK":
            u = 32 + (self.anim_frame % 2) * 16
        elif self.state == "ATTACK":
            # 攻撃は2段階 (予備動作・ヒット)
            u = 64 + (min(self.state_frame // 3, 1)) * 16
        elif self.state == "HURT":
            u = 96
        
        # v: 0(Player), 16(Enemy)
        v = 0 if self.color == 12 else 16
        
        # 反転描画
        pyxel.blt(self.x, self.y, 0, u, v, self.w * self.direction, self.h, 0)

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 12)
        self.attack_cooldown = 0
        self.hit_stop = 0

    def update(self):
        if self.hit_stop > 0:
            self.hit_stop -= 1
            return
            
        if self.state == "DIE": return

        # 移動
        if self.state != "ATTACK" and self.state != "HURT":
            move_x, move_y = 0, 0
            if pyxel.btn(pyxel.KEY_LEFT):
                move_x, self.direction = -2, -1
            elif pyxel.btn(pyxel.KEY_RIGHT):
                move_x, self.direction = 2, 1
            if pyxel.btn(pyxel.KEY_UP): move_y = -1.5
            elif pyxel.btn(pyxel.KEY_DOWN): move_y = 1.5

            self.x += move_x
            self.y += move_y
            self.x = max(0, min(SCREEN_WIDTH - self.w, self.x))
            self.y = max(FLOOR_MIN_Y, min(FLOOR_MAX_Y - self.h, self.y))

            if move_x != 0 or move_y != 0: self.state = "WALK"
            else: self.state = "IDLE"

        # 攻撃
        if pyxel.btnp(pyxel.KEY_Z) and self.state != "HURT" and self.attack_cooldown <= 0:
            self.state = "ATTACK"
            self.state_frame = 0
            self.attack_cooldown = 15

        if self.state == "ATTACK" and self.state_frame > 10:
            self.state = "IDLE"

        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        self.update_animation()

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 8)
        self.hit_stop = 0

    def update(self, player):
        if self.hit_stop > 0:
            self.hit_stop -= 1
            return
            
        if self.state == "DIE": return
        if self.state == "HURT":
            if self.state_frame > 12: self.state = "IDLE"
            self.update_animation()
            return

        # AI
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < 120:
            if abs(dy) > 2: self.y += 0.8 if dy > 0 else -0.8
            if abs(dx) > 14:
                self.x += 1 if dx > 0 else -1
                self.direction = 1 if dx > 0 else -1
                self.state = "WALK"
            else:
                self.state = "IDLE"
                if pyxel.frame_count % 50 == 0:
                    self.state = "ATTACK"
                    self.state_frame = 0
        
        if self.state == "ATTACK" and self.state_frame > 10:
            self.state = "IDLE"

        self.y = max(FLOOR_MIN_Y, min(FLOOR_MAX_Y - self.h, self.y))
        self.update_animation()

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = (pyxel.rndf(0, 1) - 0.5) * 4
        self.vy = (pyxel.rndf(0, 1) - 0.5) * 4
        self.life = 10
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pyxel.pset(self.x, self.y, self.color)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Fight - Turbo Graphics")
        self.init_assets()
        self.player = Player(20, 80)
        self.enemies = [Enemy(110, 70), Enemy(130, 90)]
        self.particles = []
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def init_assets(self):
        # --- Graphics (image 0) ---
        # Palette: 0:Trans, 1:DarkBlue, 5:DarkGray, 6:LightBlue, 7:White, 8:Red, 10:Yellow, 12:Blue, 13:Gray, 15:Skin
        
        # Player (Blue/White, High detail)
        # u=0,16 (Idle), 32,48 (Walk), 64,80 (Attack), 96 (Hurt)
        # Idle 1
        pyxel.image(0).set(0, 0, [
            "0000017777100000", "0000177777710000", "0000175555710000", "000017F7FF710000",
            "0000177FFF710000", "000001FFF1000000", "0000111111100000", "0001777777710000",
            "0001771217710000", "0001712221710000", "0000122221000000", "0000122221000000",
            "0000122221000000", "0000177077100000", "0000177077100000", "0000111011100000",
        ])
        # Idle 2 (Breathe)
        pyxel.image(0).set(16, 0, [
            "0000017777100000", "0000177777710000", "0000175555710000", "000017F7FF710000",
            "0000177FFF710000", "000001FFF1000000", "0001111111110000", "0017777777771000",
            "0017711211771000", "0017122221771000", "0000122221000000", "0000122221000000",
            "0000122221000000", "0000177077100000", "0000177077100000", "0000111011100000",
        ])
        # Attack 2 (Hit) at u=80
        pyxel.image(0).set(80, 0, [
            "0000017777100000", "0000177777710000", "0000175555710000", "000017F7FF710000",
            "0000177FFF710000", "0000117FFF100000", "0007777111111110", "007777777FFFFFF1",
            "007771217FFFFFF1", "0077122217777770", "0000122221000000", "0000122221000000",
            "0000122221000000", "0000177077100000", "0000177077100000", "0000111011100000",
        ])
        
        # Enemy (Red/Gray, v=16)
        for i in range(8):
            src = pyxel.image(0).get(i*16, 0)
            dst = [row.replace("7", "8").replace("12", "5") for row in src]
            pyxel.image(0).set(i*16, 16, dst)

        # Background (u=48, v=32)
        pyxel.image(0).set(48, 32, [
            "11111111", "15555551", "15AAAAA1", "15111111", 
            "11111111", "15111151", "15AAAA51", "15555551",
            "11111111", "15555551", "15AAAAA1", "11111111",
            "11111111", "15555551", "15AAAAA1", "11111111",
        ])

        # Sound
        pyxel.sound(0).set("g2g1", "p", "75", "f", 5) # Swing
        pyxel.sound(1).set("c2c1g1", "n", "77", "f", 8) # Hit
        pyxel.sound(2).set("c1g0c0r1", "n", "77", "f", 20) # KO
        pyxel.sound(3).set("a1a1g1g1", "s", "4", "n", 25)
        pyxel.sound(4).set("c2e2g2c3", "t", "3", "f", 25)
        pyxel.music(0).set([3], [4], [], [])

    def update(self):
        if self.player.hit_stop > 0:
            self.player.update() # Hit stop should block logic but we handle it in classes
        self.player.update()
        
        for enemy in self.enemies:
            if enemy.state == "DIE": continue
            enemy.update(self.player)
            
            # 当たり判定
            if self.player.state == "ATTACK" and self.player.state_frame == 4:
                pyxel.play(0, 0)
                if abs(self.player.y - enemy.y) < 10:
                    px = self.player.x + (14 if self.player.direction == 1 else -10)
                    if px < enemy.x + 12 and px + 8 > enemy.x:
                        # ヒット発生！
                        enemy.state, enemy.state_frame, enemy.hp = "HURT", 0, enemy.hp - 20
                        enemy.x += 6 * self.player.direction
                        self.player.hit_stop, enemy.hit_stop = 4, 4
                        pyxel.play(1, 1)
                        # 火花
                        for _ in range(5):
                            self.particles.append(Particle(px + 4, self.player.y + 8, 10))
                        if enemy.hp <= 0:
                            enemy.state = "DIE"
                            pyxel.play(2, 2)

        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self):
        pyxel.cls(1) # 夜の街
        # パララックス
        for i in range(5):
            pyxel.blt(i*40 - (pyxel.frame_count//4)%40, 30, 0, 48, 32, 8, 16, 0)
            pyxel.blt(i*40 + 20 - (pyxel.frame_count//2)%40, 50, 0, 48, 32, 8, 16, 0)

        # 地面
        pyxel.rect(0, FLOOR_MIN_Y, SCREEN_WIDTH, FLOOR_MAX_Y-FLOOR_MIN_Y, 5)
        for y in range(FLOOR_MIN_Y, FLOOR_MAX_Y, 10):
            pyxel.line(0, y, SCREEN_WIDTH, y, 1)

        entities = [self.player] + [e for e in self.enemies if e.state != "DIE"]
        entities.sort(key=lambda e: e.y)
        for e in entities: e.draw()
        for p in self.particles: p.draw()

        # UI (Gradient-like HP Bar)
        pyxel.text(5, 5, "PLAYER", 7)
        pyxel.rect(35, 5, 52, 6, 0)
        pyxel.rect(36, 6, self.player.hp // 2, 4, 11 if self.player.hp > 30 else 8)
        
        for i, enemy in enumerate(self.enemies):
            if enemy.state != "DIE":
                pyxel.rect(100, 5 + i*10, 52, 4, 0)
                pyxel.rect(101, 6 + i*10, enemy.hp // 2, 2, 8)

App()

App()
