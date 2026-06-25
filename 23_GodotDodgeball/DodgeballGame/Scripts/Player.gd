class_name Player
extends CharacterBody2D

# --- 定数・パラメータ設定 ---
@export var SPEED: float = 300.0
@export var MAX_HP: int = 100
@export var MAX_GAUGE: float = 100.0
@export var GAUGE_REGEN_RATE: float = 10.0
@export var CATCH_DURATION: float = 0.5
@export var CATCH_COOLDOWN_TIME: float = 0.5
@export var THROW_OFFSET: float = 50.0

const BALL_SCENE: PackedScene = preload("res://Scenes/Ball.tscn")

# --- 状態管理変数 ---
var hp: int = MAX_HP
var special_gauge: float = 0.0
var is_catching: bool = false
var catch_timer: float = 0.0
var catch_cooldown: float = 0.0
var prev_catch_pressed: bool = false

var player_id: int = 1
var last_direction: Vector2 = Vector2.RIGHT

# --- 入力キー管理 ---
var input_keys: Dictionary = {}

func _ready() -> void:
	if self.name == "Player2":
		player_id = 2
		last_direction = Vector2.LEFT
	
	_setup_input_keys()

func _setup_input_keys() -> void:
	# プレイヤー1と2でキーを分ける
	if player_id == 1:
		input_keys = {
			"left": KEY_A,
			"right": KEY_D,
			"up": KEY_W,
			"down": KEY_S,
			"special": KEY_SPACE,
			"catch": KEY_SHIFT
		}
	else:
		input_keys = {
			"left": KEY_LEFT,
			"right": KEY_RIGHT,
			"up": KEY_UP,
			"down": KEY_DOWN,
			"special": KEY_ENTER,
			"catch": KEY_CTRL
		}

func _physics_process(delta: float) -> void:
	_process_gauge(delta)
	_process_catch_timer(delta)
	_handle_action_inputs()
	_handle_movement()
	
	move_and_slide()

# --- 内部処理関数 ---

func _process_gauge(delta: float) -> void:
	# ゲージを自動で貯める
	if special_gauge < MAX_GAUGE:
		special_gauge += GAUGE_REGEN_RATE * delta
		if special_gauge > MAX_GAUGE:
			special_gauge = MAX_GAUGE

func _process_catch_timer(delta: float) -> void:
	# キャッチ状態のカウントダウン
	if is_catching:
		catch_timer -= delta
		if catch_timer <= 0.0:
			is_catching = false
			catch_cooldown = CATCH_COOLDOWN_TIME
			
	# クールダウンのカウントダウン
	if catch_cooldown > 0.0:
		catch_cooldown -= delta

func _handle_action_inputs() -> void:
	# キャッチの発動
	var current_catch_pressed: bool = Input.is_key_pressed(input_keys["catch"])
	if current_catch_pressed and not prev_catch_pressed and not is_catching and catch_cooldown <= 0.0:
		is_catching = true
		catch_timer = CATCH_DURATION
		print(self.name + " がキャッチの構え！")
	
	prev_catch_pressed = current_catch_pressed

	# 必殺技の発動
	if Input.is_key_pressed(input_keys["special"]) and special_gauge >= MAX_GAUGE:
		_use_special_move()

func _get_input_direction() -> Vector2:
	var move_dir := Vector2.ZERO
	if Input.is_key_pressed(input_keys["right"]): move_dir.x += 1.0
	if Input.is_key_pressed(input_keys["left"]):  move_dir.x -= 1.0
	if Input.is_key_pressed(input_keys["down"]):  move_dir.y += 1.0
	if Input.is_key_pressed(input_keys["up"]):    move_dir.y -= 1.0
	return move_dir

func _handle_movement() -> void:
	var move_dir := _get_input_direction()
	
	if move_dir != Vector2.ZERO:
		move_dir = move_dir.normalized()
		last_direction = move_dir # 最後に動いた方向を記憶する
		
	velocity = move_dir * SPEED

# --- アクション ---

func _use_special_move() -> void:
	special_gauge = 0.0
	print(self.name + " のボール投げ！")
	
	var ball: DodgeBall = BALL_SCENE.instantiate() as DodgeBall
	# 最後に動いた方向の少し先にボールを出す
	ball.position = self.position + (last_direction * THROW_OFFSET)
	ball.direction = last_direction
	ball.thrower = self # 自分（投げた人）をボールに記録する
	get_parent().add_child(ball)

func take_damage(amount: int, ball: DodgeBall) -> void:
	if is_catching:
		print(self.name + " が見事にキャッチした！")
		ball.queue_free() # ボールを消す
		special_gauge = MAX_GAUGE # 自分がボールを手に入れた（すぐ投げられる）状態になる
		is_catching = false # キャッチ成功で構えを終了
	else:
		hp -= amount
		print(self.name + " にヒット！ 残りHP: ", hp)
		
		if hp <= 0:
			print(self.name + " は力尽きた！勝負あり！")
			queue_free() # キャラクターを消滅させる
			return # これ以上処理を続けない
			
		# ボールをキャッチできなかったら、相手にボールが移る
		if ball.thrower != null:
			print("ボールが相手に戻った！")
			ball.thrower.special_gauge = MAX_GAUGE # 相手のゲージが即100になり、すぐ投げられる！
			
		ball.queue_free() # ボール自体は一度消える
