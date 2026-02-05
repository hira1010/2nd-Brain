"""
地味子PV自動生成スクリプト（簡易版）
より高速に動画を生成するため、フレーム数を削減した版
"""

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
from pathlib import Path
import subprocess
import sys

# 設定
OUTPUT_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\08_動画生成_Vidu\地味子PV")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 動画設定（高速化のため短縮版）
FPS = 30  # 30fpsに上げる
DURATION = 10  # まず10秒で試作
TOTAL_FRAMES = FPS * DURATION
WIDTH, HEIGHT = 1280, 720  # HD解像度に

print(f"🎬 地味子セクシーPV動画生成開始（試作版）")
print(f"解像度: {WIDTH}x{HEIGHT}")
print(f"フレームレート: {FPS}fps")
print(f"総フレーム数: {TOTAL_FRAMES}")
print()

# 元画像を読み込む
base_image_path = OUTPUT_DIR / "jimi_source.jpg"

if not base_image_path.exists():
    print(f"❌ 元画像が見つかりません: {base_image_path}")
    sys.exit(1)

# 画像を読み込み
print("📷 画像を読み込み中...")
base_img = Image.open(base_image_path)
base_img = base_img.convert('RGB')

# アスペクト比を保ちながらリサイズ
img_aspect = base_img.width / base_img.height
canvas_aspect = WIDTH / HEIGHT

if img_aspect > canvas_aspect:
    new_height = int(HEIGHT * 1.5)  # 大きめに
    new_width = int(new_height * img_aspect)
else:
    new_width = int(WIDTH * 1.5)
    new_height = int(new_width / img_aspect)

base_img = base_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
print(f"✓ 画像リサイズ完了: {new_width}x{new_height}")

# フレーム生成フォルダ
frames_dir = OUTPUT_DIR / "frames"
frames_dir.mkdir(exist_ok=True)

print(f"\n🎨 {TOTAL_FRAMES}フレームを生成中...")

for frame_num in range(TOTAL_FRAMES):
    progress = frame_num / TOTAL_FRAMES
    
    # 進捗表示
    if frame_num % 30 == 0:
        print(f"⏳ {int(progress * 100)}% ({frame_num}/{TOTAL_FRAMES})")
    
    # キャンバス
    canvas = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    
    # Ken Burns効果
    zoom_factor = 1.0 + progress * 0.2
    pan_x = int(np.sin(progress * np.pi * 2) * 30)
    pan_y = int(progress * 80)
    
    zoomed_width = int(new_width * zoom_factor)
    zoomed_height = int(new_height * zoom_factor)
    zoomed_img = base_img.resize((zoomed_width, zoomed_height), Image.Resampling.LANCZOS)
    
    offset_x = (WIDTH - zoomed_width) // 2 + pan_x
    offset_y = (HEIGHT - zoomed_height) // 2 - pan_y
    
    canvas.paste(zoomed_img, (offset_x, offset_y))
    
    # カラーグレーディング
    if progress < 0.33:
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (255, 200, 150))
        canvas = Image.blend(canvas, overlay, 0.1)
    elif progress < 0.66:
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (120, 160, 200))
        canvas = Image.blend(canvas, overlay, 0.08)
    else:
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (255, 180, 200))
        canvas = Image.blend(canvas, overlay, 0.12)
    
    # ビネット
    mask = Image.new('L', (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    for i in range(WIDTH // 2):
        alpha = int(255 * (i / (WIDTH / 2)))
        draw.ellipse([WIDTH//2 - i*2, HEIGHT//2 - i*1.2, WIDTH//2 + i*2, HEIGHT//2 + i*1.2], 
                     fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=80))
    
    black = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    canvas = Image.composite(canvas, black, mask)
    
    # 保存
    canvas.save(frames_dir / f"frame_{frame_num:05d}.jpg", 'JPEG', quality=90, optimize=True)

print(f"\n✅ 全{TOTAL_FRAMES}フレーム生成完了！")
print(f"📁 フレーム: {frames_dir}")

# ffmpegで動画に変換
print(f"\n🎬 動画に変換中...")
output_video = OUTPUT_DIR / "jimi_pv_test.mp4"

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", str(frames_dir / "frame_%05d.jpg"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "23",
    "-preset", "fast",
    str(output_video)
]

try:
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
    print(f"\n✅ 動画生成完了！")
    print(f"📹 出力: {output_video}")
except subprocess.CalledProcessError as e:
    print(f"❌ ffmpegエラー: {e}")
    print("手動コマンド:")
    print(f'ffmpeg -framerate {FPS} -i "{frames_dir}/frame_%05d.jpg" -c:v libx264 -pix_fmt yuv420p -crf 23 "{output_video}"')
except FileNotFoundError:
    print("⚠ ffmpegが見つかりません。手動で変換してください:")
    print(f'ffmpeg -framerate {FPS} -i "{frames_dir}/frame_%05d.jpg" -c:v libx264 -pix_fmt yuv420p -crf 23 "{output_video}"')
