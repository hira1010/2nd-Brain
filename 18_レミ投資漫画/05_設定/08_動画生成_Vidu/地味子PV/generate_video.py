"""
地味子セクシーPV動画生成スクリプト
提供された画像から1分間のプロモーション動画を生成
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import os
from pathlib import Path

# 設定
OUTPUT_DIR = Path(r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\05_設定\08_動画生成_Vidu\地味子PV")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 動画設定
FPS = 24
DURATION = 60  # 秒
TOTAL_FRAMES = FPS * DURATION
WIDTH, HEIGHT = 1920, 1080

print(f"🎬 地味子セクシーPV動画生成開始")
print(f"解像度: {WIDTH}x{HEIGHT}")
print(f"フレームレート: {FPS}fps")
print(f"総フレーム数: {TOTAL_FRAMES}")
print(f"出力ディレクトリ: {OUTPUT_DIR}")
print()

# 元画像を読み込む（ユーザー提供画像のパスを指定）
# 注: 実際の画像パスはユーザーに確認が必要
base_image_path = OUTPUT_DIR / "jimi_source.jpg"

if not base_image_path.exists():
    print(f"⚠ 元画像が見つかりません: {base_image_path}")
    print("📝 画像を配置してください。")
    # ダミー画像を生成
    dummy_img = Image.new('RGB', (1920, 1080), color=(40, 40, 60))
    draw = ImageDraw.Draw(dummy_img)
    draw.text((WIDTH//2 - 200, HEIGHT//2), "地味子の画像を配置してください", fill=(255,255,255))
    dummy_img.save(base_image_path)
    print(f"✓ ダミー画像を生成: {base_image_path}")

# 画像を読み込み
print("📷 画像を読み込み中...")
base_img = Image.open(base_image_path)
base_img = base_img.convert('RGB')

# アスペクト比を保ちながらリサイズ
img_aspect = base_img.width / base_img.height
canvas_aspect = WIDTH / HEIGHT

if img_aspect > canvas_aspect:
    new_height = HEIGHT
    new_width = int(new_height * img_aspect)
else:
    new_width = WIDTH
    new_height = int(new_width / img_aspect)

base_img = base_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
print(f"✓ 画像リサイズ完了: {new_width}x{new_height}")

# フレーム生成フォルダ
frames_dir = OUTPUT_DIR / "frames"
frames_dir.mkdir(exist_ok=True)

print(f"\n🎨 {TOTAL_FRAMES}フレームを生成中...")

for frame_num in range(TOTAL_FRAMES):
    progress = frame_num / TOTAL_FRAMES
    
    # 進捗表示（10%ごと）
    if frame_num % (TOTAL_FRAMES // 10) == 0:
        print(f"⏳ {int(progress * 100)}% 完了 ({frame_num}/{TOTAL_FRAMES})")
    
    # 新しいキャンバスを作成
    canvas = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    
    # Ken Burns効果: ズーム＆パン
    zoom_factor = 1.0 + progress * 0.3  # 1.0 → 1.3
    pan_x_offset = int(np.sin(progress * np.pi * 2) * 50)  # 左右パン
    pan_y_offset = int(progress * 100)  # 上方向パン
    
    # 拡大後のサイズ
    zoomed_width = int(new_width * zoom_factor)
    zoomed_height = int(new_height * zoom_factor)
    zoomed_img = base_img.resize((zoomed_width, zoomed_height), Image.Resampling.LANCZOS)
    
    # 配置位置計算
    offset_x = (WIDTH - zoomed_width) // 2 + pan_x_offset
    offset_y = (HEIGHT - zoomed_height) // 2 - pan_y_offset
    
    # 画像を貼り付け
    canvas.paste(zoomed_img, (offset_x, offset_y))
    
    # カラーグレーディング（時間経過で変化）
    if progress < 0.33:
        # 序盤: ウォームトーン
        enhancer = ImageEnhance.Color(canvas)
        canvas = enhancer.enhance(1.2)
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (255, 200, 150))
        canvas = Image.blend(canvas, overlay, 0.1)
    elif progress < 0.66:
        # 中盤: ティール＆オレンジ
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (100, 150, 200))
        canvas = Image.blend(canvas, overlay, 0.08)
    else:
        # 終盤: ロマンティックピンク
        overlay = Image.new('RGB', (WIDTH, HEIGHT), (255, 180, 200))
        canvas = Image.blend(canvas, overlay, 0.12)
    
    # ビネット効果
    vignette = Image.new('L', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(vignette)
    for i in range(min(WIDTH, HEIGHT) // 2):
        alpha = int(255 * (1 - (i / (min(WIDTH, HEIGHT) / 2)) ** 2))
        draw.ellipse([WIDTH//2 - i*2, HEIGHT//2 - i*1.5, WIDTH//2 + i*2, HEIGHT//2 + i*1.5], 
                     fill=alpha)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=100))
    
    # ビネットを適用
    black = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    canvas = Image.composite(canvas, black, vignette)
    
    # フレームを保存
    frame_path = frames_dir / f"frame_{frame_num:05d}.png"
    canvas.save(frame_path, 'PNG', optimize=True)

print(f"\n✅ 全{TOTAL_FRAMES}フレーム生成完了！")
print(f"📁 フレーム保存先: {frames_dir}")
print(f"\n🎬 次のステップ: ffmpegで動画に変換")
print(f"コマンド例:")
print(f'ffmpeg -framerate {FPS} -i "{frames_dir}/frame_%05d.png" -c:v libx264 -pix_fmt yuv420p -crf 18 "{OUTPUT_DIR}/jimi_pv.mp4"')
