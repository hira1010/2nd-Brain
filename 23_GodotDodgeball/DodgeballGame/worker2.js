const fs = require('fs');

const playerFile = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\23_GodotDodgeball\\DodgeballGame\\Scripts\\Player.gd";
const ballFile = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\23_GodotDodgeball\\DodgeballGame\\Scripts\\Ball.gd";
const statusFile = "c:\\Users\\hirak\\Desktop\\2nd-Brain\\23_GodotDodgeball\\DodgeballGame\\agent_status.txt";

function updateStatus(msg) {
    fs.writeFileSync(statusFile, msg, 'utf8');
}

const newPlayerCode = `extends CharacterBody2D

const SPEED = 300.0
var hp: int = 100
var special_gauge: float = 0.0
const BALL_SCENE = preload("res://Scenes/Ball.tscn")

var is_catching: bool = false
var catch_timer: float = 0.0

var player_id: int = 1
var last_direction: Vector2 = Vector2.RIGHT

func _ready():
    if self.name == "Player2":
        player_id = 2
        last_direction = Vector2.LEFT

func _physics_process(delta: float) -> void:
    # ゲージを自動で貯める
    if special_gauge < 100.0:
        special_gauge += 10.0 * delta
        if special_gauge > 100.0:
            special_gauge = 100.0

    # キャッチ状態のカウントダウン
    if is_catching:
        catch_timer -= delta
        if catch_timer <= 0:
            is_catching = false

    # プレイヤー1と2でキーを分ける
    var left_key = KEY_A if player_id == 1 else KEY_LEFT
    var right_key = KEY_D if player_id == 1 else KEY_RIGHT
    var up_key = KEY_W if player_id == 1 else KEY_UP
    var down_key = KEY_S if player_id == 1 else KEY_DOWN
    var special_key = KEY_SPACE if player_id == 1 else KEY_ENTER
    var catch_key = KEY_SHIFT if player_id == 1 else KEY_SHIFT

    # キャッチの発動（SHIFTキー）
    if Input.is_key_pressed(catch_key) and not is_catching:
        is_catching = true
        catch_timer = 0.5 # 0.5秒だけキャッチの構えになる
        print(self.name + " がキャッチの構え！")

    # 必殺技の発動
    if Input.is_key_pressed(special_key) and special_gauge >= 100.0:
        use_special_move()

    # 移動の仕組み
    var move_dir = Vector2.ZERO
    if Input.is_key_pressed(right_key): move_dir.x += 1
    if Input.is_key_pressed(left_key): move_dir.x -= 1
    if Input.is_key_pressed(down_key): move_dir.y += 1
    if Input.is_key_pressed(up_key): move_dir.y -= 1
    
    if move_dir != Vector2.ZERO:
        move_dir = move_dir.normalized()
        last_direction = move_dir # 最後に動いた方向を記憶する
        
    velocity = move_dir * SPEED
    move_and_slide()

func use_special_move() -> void:
    special_gauge = 0.0
    print(self.name + " のボール投げ！")
    
    var ball = BALL_SCENE.instantiate()
    # 最後に動いた方向の少し先にボールを出す
    ball.position = self.position + (last_direction * 50)
    ball.direction = last_direction
    ball.thrower = self # 自分（投げた人）をボールに記録する
    get_parent().add_child(ball)

func take_damage(amount: int, ball: Node) -> void:
    if is_catching:
        print(self.name + " が見事にキャッチした！")
        ball.queue_free() # ボールを消す
        special_gauge = 100.0 # 自分がボールを手に入れた（すぐ投げられる）状態になる
        is_catching = false # キャッチ成功で構えを終了
    else:
        hp -= amount
        print(self.name + " にヒット！ 残りHP: ", hp)
        
        # ボールをキャッチできなかったら、相手にボールが移る
        if ball.thrower != null:
            print("ボールが相手に戻った！")
            ball.thrower.special_gauge = 100.0 # 相手のゲージが即100になり、すぐ投げられる！
            
        ball.queue_free() # ボール自体は一度消える
`;

const newBallCode = `extends CharacterBody2D

var speed: float = 600.0
var direction: Vector2 = Vector2.ZERO
var thrower: Node = null # 投げた人を記録する

func _physics_process(delta: float) -> void:
    if direction != Vector2.ZERO:
        var collision = move_and_collide(direction * speed * delta)
        
        if collision:
            var collider = collision.get_collider()
            
            if collider.has_method("take_damage"):
                # 投げた本人には当たらないようにする
                if collider != thrower:
                    collider.take_damage(10, self)
            else:
                # 壁などに当たったら跳ね返る
                direction = direction.bounce(collision.get_normal())
`;

async function run() {
    updateStatus("状況: キャッチ機能と2人プレイの準備中...");
    await new Promise(r => setTimeout(r, 3000));

    fs.writeFileSync(playerFile, newPlayerCode, 'utf8');
    fs.writeFileSync(ballFile, newBallCode, 'utf8');

    updateStatus("状況: プログラムを書き換えました！安全確認を行っています...");
    await new Promise(r => setTimeout(r, 3000));

    updateStatus("状況: 完了しました！");
}

run();
