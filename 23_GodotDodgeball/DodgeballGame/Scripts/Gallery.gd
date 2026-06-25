extends Control

const GALLERY_DIR = "res://Assets/Gallery/"

@onready var grid_container: GridContainer = $ScrollContainer/GridContainer
@onready var back_button: Button = $BackButton
@onready var detail_view: Control = $DetailView
@onready var detail_texture: TextureRect = $DetailView/TextureRect
@onready var progress_label: Label = $ProgressLabel

func _ready() -> void:
	detail_view.visible = false
	_setup_gallery()

func _setup_gallery() -> void:
	for child in grid_container.get_children():
		child.queue_free()
	
	var total_count = SaveManager.gallery_images.size()
	var unlocked_count = SaveManager.unlocked_indices.size()
	
	progress_label.text = "解放状況: %d / %d" % [unlocked_count, total_count]
	
	for i in range(total_count):
		var btn = Button.new()
		btn.custom_minimum_size = Vector2(150, 150)
		btn.expand_icon = true
		btn.focus_mode = Control.FOCUS_NONE
		
		if SaveManager.unlocked_indices.has(i):
			var img_path = GALLERY_DIR + SaveManager.gallery_images[i]
			var tex = load(img_path)
			btn.icon = tex
			btn.pressed.connect(_on_image_pressed.bind(tex))
		else:
			btn.text = "？"
			btn.disabled = true
			# 少し見栄えを良くするためにグレーアウト
			btn.modulate = Color(0.4, 0.4, 0.4, 1.0)
		
		grid_container.add_child(btn)

func _on_image_pressed(texture: Texture) -> void:
	detail_texture.texture = texture
	detail_view.visible = true

func _on_detail_view_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		detail_view.visible = false

func _on_back_button_pressed() -> void:
	get_tree().change_scene_to_file("res://Scenes/Title.tscn")
