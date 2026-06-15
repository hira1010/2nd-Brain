import os
from PIL import Image

input_path = r"C:\Users\hirak\.gemini\antigravity-ide\brain\67e34be1-7ca3-46fc-8983-191829bd8d70\rpg_chibi_pixel_sprite_1781185328327.png"
output_path = r"C:\Users\hirak\.gemini\antigravity-ide\brain\67e34be1-7ca3-46fc-8983-191829bd8d70\rpg_chibi_pixel_sprite_formatted.png"

try:
    img = Image.open(input_path)
    width, height = img.size
    
    # AI画像から縦4横3のアスペクト比(144:192 = 3:4)で中央を切り抜く
    target_ratio = 144 / 192
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        new_height = height
        left = (width - new_width) / 2
        top = 0
        right = left + new_width
        bottom = height
    else:
        new_width = width
        new_height = int(width / target_ratio)
        left = 0
        top = (height - new_height) / 2
        right = width
        bottom = top + new_height

    img_cropped = img.crop((left, top, right, bottom))
    
    # RPGツクールMZの1キャラクター分の正確なサイズにリサイズ (横144px × 縦192px)
    img_resized = img_cropped.resize((144, 192), Image.Resampling.LANCZOS)
    
    # 白背景を透過処理
    img_rgba = img_resized.convert("RGBA")
    data = img_rgba.getdata()
    new_data = []
    for item in data:
        # 白(240以上)を透明にする
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img_rgba.putdata(new_data)
    
    img_rgba.save(output_path, "PNG")
    print(f"Success! Formatted image saved to: {output_path}")

except Exception as e:
    print(f"Error: {e}")
