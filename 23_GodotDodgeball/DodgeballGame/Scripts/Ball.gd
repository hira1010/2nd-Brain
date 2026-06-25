class_name DodgeBall
extends CharacterBody2D

# --- 定数・パラメータ設定 ---
@export var SPEED: float = 600.0
@export var DAMAGE_AMOUNT: int = 10

# --- 状態管理変数 ---
var direction: Vector2 = Vector2.ZERO
var thrower: Player = null # 投げた人を記録する

func _physics_process(delta: float) -> void:
	if direction != Vector2.ZERO:
		var collision: KinematicCollision2D = move_and_collide(direction * SPEED * delta)
		if collision:
			_handle_collision(collision)

# --- 内部処理関数 ---

func _handle_collision(collision: KinematicCollision2D) -> void:
	var collider: Object = collision.get_collider()
	
	if collider is Player:
		var player := collider as Player
		# 投げた本人には当たらないようにする
		if player != thrower:
			player.take_damage(DAMAGE_AMOUNT, self)
	else:
		# 壁などに当たったら跳ね返る
		direction = direction.bounce(collision.get_normal())
