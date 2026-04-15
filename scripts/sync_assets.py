import os
import shutil
from pathlib import Path

# --- 設定 ---
ROOT_DIR = Path(__file__).resolve().parent.parent

# 各エンジンのアセットパス定義
PROJECTS = {
    "RENPY": {
        "img": ROOT_DIR / "Engine_RenPy/game/images",
        "audio": ROOT_DIR / "Engine_RenPy/game/audio"
    },
    "RPG_MAKER": {
        "img": ROOT_DIR / "Engine_RPGMaker_MZ/img/pictures",
        "audio": ROOT_DIR / "Engine_RPGMaker_MZ/audio/se"
    },
    "TYRANO": {
        "img": ROOT_DIR / "Engine_TyranoBuilder/data/fgimage",
        "audio": ROOT_DIR / "Engine_TyranoBuilder/data/sound"
    },
    "TWINE": {
        "img": ROOT_DIR / "Engine_Twine_Web/images",
        "audio": ROOT_DIR / "Engine_Twine_Web/audio"
    }
}

# 同期・リネームマップ
# (ソースファイル名: ターゲットファイル名)
ASSET_MAP = {
    "images": {
        "heroine1.png": ["heroine1.png", "heroine_rank1.png", "Heroine_1.png"],
        "heroine2.png": ["heroine2.png", "heroine_rank2.png", "Heroine_2.png"],
        "heroine3.png": ["heroine3.png", "heroine_rank3.png", "Heroine_3.png"],
        "heroine_blush.png": ["heroine_blush.png", "heroine_rank1_blush.png", "Heroine_1_Blush.png"],
        "heroine_excited.png": ["heroine_excited.png", "heroine_rank1_excited.png", "Heroine_1_Excited.png"],
        "bg_classroom.png": ["bg_classroom.png", "bg classroom_day.png", "Background_Classroom.png"],
        "heart.png": ["heart.png", "effect_heart.png"],
        "lotion.png": ["lotion.png"],
        "vibrator.png": ["vibrator.png"],
        "high_vibe.png": ["high_vibe.png", "item_super_vibe.png", "SuperVibe.png"],
        "aroma_oil.png": ["aroma_oil.png", "item_oil.png", "AromaOil.png"]
    },
    "audio": {
        "vo_kyoko_moan_ear.ogg": ["vo_kyoko_moan_ear.ogg", "ear.ogg", "ear.mp3"],
        "vo_kyoko_moan_chest.ogg": ["vo_kyoko_moan_chest.ogg", "chest.ogg", "chest.mp3"],
        "AnyConv.com__137そこ…っ！.ogg": ["crotch.ogg", "crotch.mp3", "crotch_moan.ogg"]
    }
}

def sync():
    print("--- Asset Syncing Started ---")
    
    # 基準となるソースフォルダ（今回は TyranoBuilder のものを基準とする）
    source_img_dir = PROJECTS["TYRANO"]["img"]
    # bgimage フォルダも考慮
    source_bg_dir = ROOT_DIR / "Engine_TyranoBuilder/data/bgimage"
    source_audio_dir = PROJECTS["TYRANO"]["audio"]

    # 画像の同期 (通常画像)
    for src_name, dest_names in ASSET_MAP["images"].items():
        # fgimage または bgimage から探す
        src_path = source_img_dir / src_name
        if not src_path.exists():
            src_path = source_bg_dir / src_name
            
        if not src_path.exists():
            print(f"[SKIP] Source missing: {src_name}")
            continue
            
        for project_name, paths in PROJECTS.items():
            for dest_name in dest_names:
                # 送り先フォルダを決定
                dest_path = paths["img"] / dest_name
                
                # 自分自身へのコピーはスキップ
                if src_path == dest_path: continue
                
                try:
                    os.makedirs(dest_path.parent, exist_ok=True)
                    shutil.copy2(src_path, dest_path)
                    print(f"[OK] Synced {src_name} -> {project_name}:{dest_name}")
                except Exception as e:
                    print(f"[ERR] Failed to sync {src_name} to {project_name}: {e}")

    # 音声の同期
    for src_name, dest_names in ASSET_MAP["audio"].items():
        src_path = PROJECTS["RPG_MAKER"]["audio"] / src_name
        if not src_path.exists():
            print(f"[SKIP] Audio source missing: {src_name}")
            continue
            
        for project_name, paths in PROJECTS.items():
            for dest_name in dest_names:
                dest_path = paths["audio"] / dest_name
                # Twineなどフォルダが分かれている場合のため
                os.makedirs(dest_path.parent, exist_ok=True)
                
                if src_path == dest_path: continue
                
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"[OK] Audio Synced {src_name} -> {project_name}:{dest_name}")
                except Exception as e:
                    print(f"[ERR] Failed to sync audio {src_name}: {e}")

    print("--- Asset Syncing Completed ---")

if __name__ == "__main__":
    sync()
