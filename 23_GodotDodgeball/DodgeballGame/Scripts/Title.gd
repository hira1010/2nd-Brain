extends Control

func _ready() -> void:
	if OS.get_cmdline_args().has("--auto-test"):
		print("[TEST] タイトルから対戦画面へ自動遷移します。")
		await get_tree().process_frame
		_on_battle_button_pressed()

func _on_battle_button_pressed() -> void:
	get_tree().change_scene_to_file("res://Scenes/Main.tscn")

func _on_gallery_button_pressed() -> void:
	get_tree().change_scene_to_file("res://Scenes/Gallery.tscn")

func _on_exit_button_pressed() -> void:
	get_tree().quit()

