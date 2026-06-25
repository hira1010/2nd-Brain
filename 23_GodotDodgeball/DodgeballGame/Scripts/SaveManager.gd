extends Node

const SAVE_PATH = "user://save_data.json"
const GALLERY_DIR = "res://Assets/Gallery/"

var gallery_images: Array[String] = []
var unlocked_indices: Array = []

func _ready() -> void:
	_scan_gallery_images()
	load_save_data()

func _scan_gallery_images() -> void:
	gallery_images.clear()
	var dir = DirAccess.open(GALLERY_DIR)
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if not dir.current_is_dir() and file_name.ends_with(".png"):
				gallery_images.append(file_name)
			file_name = dir.get_next()
		dir.list_dir_end()
		gallery_images.sort()
	else:
		print("ギャラリーディレクトリが開けませんでした: ", GALLERY_DIR)

func save_data() -> void:
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		var data = {
			"unlocked_indices": unlocked_indices
		}
		var json_string = JSON.stringify(data)
		file.store_string(json_string)
		file.close()

func load_save_data() -> void:
	unlocked_indices.clear()
	if FileAccess.file_exists(SAVE_PATH):
		var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
		if file:
			var json_string = file.get_as_text()
			file.close()
			var json = JSON.new()
			var error = json.parse(json_string)
			if error == OK:
				var data = json.get_data()
				if data is Dictionary and data.has("unlocked_indices"):
					unlocked_indices = data["unlocked_indices"]
					return
	unlocked_indices = []

func unlock_next_image() -> String:
	var next_idx = -1
	for i in range(gallery_images.size()):
		if not unlocked_indices.has(i):
			next_idx = i
			break
	
	if next_idx != -1:
		unlocked_indices.append(next_idx)
		save_data()
		return gallery_images[next_idx]
	return ""
