# ゲームの基本設定

# ゲームの名称
define config.name = _("ヒロイン密着クリック＆チェキ経済ADV")
define gui.show_name = True

# バージョン
define config.version = "1.0"

# ウィンドウのタイトル
define config.window_title = _("ヒロイン密着クリック＆チェキ経済ADV")

# 画面サイズ
define config.screen_width = 1280
define config.screen_height = 720

# データの保存場所
define config.save_directory = "23_HeroineAdv-123456789"

# アイコン画像（後で設定可能）
# define config.window_icon = "gui/window_icon.png"

# デバッグ用
define config.developer = True

# トランジション
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

# フォント
# define config.font_replacement_map["font.ttf", True, False] = ("font_bold.ttf", False, False)
