extends CharacterBody2D

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
