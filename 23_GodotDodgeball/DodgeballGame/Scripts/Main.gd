extends Node2D

@onready var result_panel: Control = $UI/ResultPanel
@onready var winner_text: Label = $UI/ResultPanel/WinnerText
@onready var unlock_group: Control = $UI/ResultPanel/UnlockGroup
@onready var unlock_texture: TextureRect = $UI/ResultPanel/UnlockGroup/TextureRect
@onready var cut_in_panel: Control = $UI/CutInPanel

func _ready() -> void:
	$Player1.defeated.connect(_on_player_defeated)
	$Player2.defeated.connect(_on_player_defeated)
	$Player1.special_thrown.connect(_on_player_special_thrown)
	$Player2.special_thrown.connect(_on_player_special_thrown)
	
	if OS.get_cmdline_args().has("--auto-test"):
		print("[TEST] 自動対戦テストを開始します...")
		await get_tree().create_timer(0.5).timeout
		_run_auto_test()

func _on_pause_button_pressed() -> void:
	get_tree().paused = not get_tree().paused

func _on_player_defeated(defeated_player: Player) -> void:
	var winner_id = 2 if defeated_player.player_id == 1 else 1
	winner_text.text = "PLAYER %d WIN!" % winner_id
	
	if winner_id == 1:
		var unlocked_file = SaveManager.unlock_next_image()
		if unlocked_file != "":
			unlock_group.visible = true
			var img_path = SaveManager.GALLERY_DIR + unlocked_file
			unlock_texture.texture = load(img_path)
		else:
			unlock_group.visible = false
	else:
		unlock_group.visible = false
		
	result_panel.visible = true
	get_tree().paused = true

func _on_player_special_thrown(player: Player) -> void:
	cut_in_panel.get_node("Label").text = "必殺：PLAYER %d アタック！" % player.player_id
	cut_in_panel.visible = true
	Engine.time_scale = 0.25
	await get_tree().create_timer(0.3, true, false, true).timeout
	Engine.time_scale = 1.0
	cut_in_panel.visible = false

func _run_auto_test() -> void:
	print("[TEST] プレイヤー2を敗北させます...")
	var ball_scene = load("res://Scenes/Ball.tscn")
	var dummy_ball = ball_scene.instantiate()
	$Player2.take_damage($Player2.hp, dummy_ball)
	
	await get_tree().process_frame
	if result_panel.visible:
		print("[TEST] ✅ 結果パネルの表示に成功！")
		if "PLAYER 1 WIN!" in winner_text.text:
			print("[TEST] ✅ プレイヤー1の勝利判定に成功！")
			print("[TEST] 現在のアンロック画像数: ", SaveManager.unlocked_indices.size())
			print("[TEST] 🎉 テストがすべて正常に完了しました！")
			get_tree().quit(0)
			return
	
	print("[TEST] ❌ テスト中にエラーが発生しました。")
	get_tree().quit(1)

func _on_retry_button_pressed() -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()

func _on_title_button_pressed() -> void:
	get_tree().paused = false
	get_tree().change_scene_to_file("res://Scenes/Title.tscn")
