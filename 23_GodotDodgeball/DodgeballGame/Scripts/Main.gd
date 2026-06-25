extends Node2D

func _on_pause_button_pressed() -> void:
	get_tree().paused = not get_tree().paused
