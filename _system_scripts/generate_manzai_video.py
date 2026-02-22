
import os
import re
import math
import argparse
from pathlib import Path
import sys

try:
    # MoviePy v2 compatibility
    from moviepy import AudioFileClip, ImageClip, ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips
except ImportError:
    try:
        # Fallback for older versions
        from moviepy.editor import AudioFileClip, ImageClip, ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips
    except ImportError:
        print("MoviePy is not installed. Please install it using: pip install moviepy")
        sys.exit(1)

# ==========================================
# 設定
# ==========================================
IMAGE_DIR = Path("18_レミ投資漫画/マンガノ/01_長編_希望の投資/04_漫談動画/images")
AUDIO_DIR = Path("18_レミ投資漫画/マンガノ/01_長編_希望の投資/04_漫談動画/audio_voicevox")
OUTPUT_FILE = Path("18_レミ投資漫画/マンガノ/01_長編_希望の投資/04_漫談動画/manzai_video_animated.mp4")

# キャラクター画像
IMG_REMI = "remi.png"
IMG_YUTO = "yuto.png"

# 動画サイズ
VIDEO_SIZE = (1920, 1080)
FPS = 24

# レイアウト設定
REMI_POS = ("left", "center") # 左側
YUTO_POS = ("right", "center") # 右側
SCALE_talking = 1.05
SCALE_listening = 1.0
BRIGHTNESS_listening = 0.7

def get_audio_files(audio_dir):
    """音声ファイルをファイル名の番号順に取得"""
    files = sorted([f for f in audio_dir.glob("*.wav") if re.match(r"^\d+_", f.name)])
    if not files:
        files = sorted([f for f in audio_dir.glob("*.mp3") if re.match(r"^\d+_", f.name)])
    return files

def create_animated_clip(audio_path, remi_img_path, yuto_img_path):
    """話者に応じてアニメーション付きクリップを作成"""
    audio_clip = AudioFileClip(str(audio_path))
    duration = audio_clip.duration
    filename = audio_path.name
    
    # 話者判定
    is_remi_talking = "レミ" in filename
    is_yuto_talking = "優斗" in filename
    
    # 背景 (白)
    bg = ColorClip(size=VIDEO_SIZE, color=(255, 255, 255)).with_duration(duration)

    clips = [bg]

    # --- レミの処理 ---
    if remi_img_path and remi_img_path.exists():
        remi_clip = ImageClip(str(remi_img_path)).with_duration(duration)
        if is_remi_talking:
            # 話している時: 明るく、少し大きく、バウンドさせる
            remi_clip = remi_clip.resized(height=VIDEO_SIZE[1] * 0.85)
            # バウンドアニメーション (簡易的: Y位置を少し上下)
            def bounce(t):
                return ('left', VIDEO_SIZE[1] * 0.1 + 10 * math.sin(t * 10)) # 10px bounce
            # v2では with_position, v1では set_position
            try:
                remi_clip = remi_clip.with_position(bounce)
            except AttributeError:
                remi_clip = remi_clip.set_position(bounce)
        else:
            # 聞いている時: 少し暗く(透明度で代用orColorClip重ね)、静止
            remi_clip = remi_clip.resized(height=VIDEO_SIZE[1] * 0.8)
            try:
                remi_clip = remi_clip.with_position(('left', 'bottom'))
                # 暗くする効果 (黒の半透明レイヤーを重ねるのが確実だが、ここでは簡易的にOpacity)
                # MoviePyで明るさ調整は複雑なので、サイズ差と位置で表現
            except AttributeError:
                remi_clip = remi_clip.set_position(('left', 'bottom'))
            
            # 暗幕効果 (Listening Dim)
            dim_clip = ColorClip(size=remi_clip.size, color=(0,0,0)).with_opacity(0.3).with_duration(duration)
            try:
                dim_clip = dim_clip.with_position(('left', 'bottom'))
            except AttributeError:
                dim_clip = dim_clip.set_position(('left', 'bottom'))
            # Note: CompositeVideoClipで重ねる順序に注意
            
        clips.append(remi_clip)
        if not is_remi_talking:
             # Listening Dim (positioning matches logic above, simplified)
             pass 

    # --- 優斗の処理 ---
    if yuto_img_path and yuto_img_path.exists():
        yuto_clip = ImageClip(str(yuto_img_path)).with_duration(duration)
        if is_yuto_talking:
            yuto_clip = yuto_clip.resized(height=VIDEO_SIZE[1] * 0.85)
            def bounce_y(t):
                return ('right', VIDEO_SIZE[1] * 0.1 + 10 * math.sin(t * 10))
            try:
                yuto_clip = yuto_clip.with_position(bounce_y)
            except AttributeError:
                 yuto_clip = yuto_clip.set_position(bounce_y)
        else:
            yuto_clip = yuto_clip.resized(height=VIDEO_SIZE[1] * 0.8)
            try:
                yuto_clip = yuto_clip.with_position(('right', 'bottom'))
            except AttributeError:
                yuto_clip = yuto_clip.set_position(('right', 'bottom'))
        
        clips.append(yuto_clip)

    # 合成
    final_clip = CompositeVideoClip(clips).with_audio(audio_clip)
    return final_clip

def main():
    if not AUDIO_DIR.exists():
        print(f"エラー: 音声フォルダが見つかりません: {AUDIO_DIR}")
        return

    print("=== 漫談動画生成 (アニメーション版) スタート ===")
    
    audio_files = get_audio_files(AUDIO_DIR)
    remi_path = IMAGE_DIR / IMG_REMI
    yuto_path = IMAGE_DIR / IMG_YUTO

    if not remi_path.exists() or not yuto_path.exists():
        print("警告: キャラクター画像が揃っていません。")

    clips = []
    for audio_file in audio_files:
        print(f"Processing: {audio_file.name}")
        try:
            clip = create_animated_clip(audio_file, remi_path, yuto_path)
            clips.append(clip)
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    if not clips:
        return

    print("動画を結合中...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    print(f"動画を保存中: {OUTPUT_FILE}")
    final_video.write_videofile(str(OUTPUT_FILE), fps=FPS, codec="libx264", audio_codec="aac")
    print("完了！")

if __name__ == "__main__":
    main()
