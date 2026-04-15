# definitions.rpy - Ver 8.0 密着クリック＆チェキ経済版

# ==========================================
# 1. 立ち絵と背景の定義
# ==========================================

# 立ち絵の自動切り替え定義（ランクに連動）
# ※既存のアセット名 (heroine_rank1.png 等) に合わせて調整
image heroine_main = ConditionSwitch(
    "p_rank == 1", "images/heroine_rank1.png",
    "p_rank == 2", "images/heroine_rank2.png",
    "p_rank == 3", "images/heroine_rank3.png",
)

# 背景の定義
image bg_classroom = "images/bg classroom_day.png"

# ==========================================
# 2. 演出・アニメーション (Transforms)
# ==========================================

# 胸の揺れアニメーション（ATL）
transform breast_shake:
    yoffset 0
    easein 0.1 yoffset 8
    easeout 0.1 yoffset 0

# クリック時の波紋エフェクト
transform ripple_effect:
    alpha 1.0 zoom 0.5
    parallel:
        easeout 0.5 alpha 0.0
    parallel:
        easeout 0.5 zoom 1.2

# ==========================================
# 3. 変数のデフォルト値 (State)
# ==========================================

default p_intimacy = 0.0    # 親密度
default p_pleasure = 0.0    # 快感度
default p_rank = 1          # ランク
default p_money = 0         # 所持金
default p_anger = 0         # 怒り蓄積
default is_punishment = False

# 装備品フラグ
default has_ribbon = False   # 親密度 1.5倍
default has_perfume = False  # 快感度 2.0倍
default has_lens = False     # 売却価格 1.2倍

# その他・演出用アセット
image white = Solid("#ffffff")

# ==========================================
# 4. 配置データ (Configuration)
# ==========================================

# 部位ごとの設定（座標、サイズ、上昇値、音声、演出）を一括管理
define PARTS_CONFIG = {
    "ear": {
        "name": "耳",
        "pos": (570, 100),
        "size": (150, 150),
        "inc_int": 1.0,
        "inc_ple": 0.0,
        "voice": "ear.wav",
        "shake": False
    },
    "chest": {
        "name": "胸",
        "pos": (510, 270),
        "size": (280, 200),
        "inc_int": 2.0,
        "inc_ple": 5.0,
        "voice": "chest.wav",
        "shake": True
    },
    "crotch": {
        "name": "股間",
        "pos": (550, 570),
        "size": (180, 200),
        "inc_int": 5.0,
        "inc_ple": 10.0,
        "voice": "crotch.wav",
        "shake": False
    }
}


