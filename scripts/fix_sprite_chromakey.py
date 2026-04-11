from PIL import Image
import os

# New green sprite
input_path = r'C:\Users\hirak\.gemini\antigravity\brain\59097361-dbd9-4c28-b843-49784abccbc4\heroine_sprite_chromakey_green_1774858516765.png'
# Final project path
output_path = r'c:\Users\hirak\Desktop\2nd-Brain\05_RPG制作\img\characters\$Heroine.png'

if not os.path.exists(input_path):
    print(f"Input file not found: {input_path}")
    exit(1)

# 1. Load Original
img = Image.open(input_path).convert('RGBA')
data = img.getdata()

# 2. Chroma Key Replacement
# The background is bright green (0, 255, 0)
# We use a small threshold to be safe
new_data = []
for item in data:
    r, g, b, a = item
    # If it's very green and r, b are low
    if g > 180 and r < 80 and b < 80:
        new_data.append((0, 0, 0, 0)) # Transparent
    else:
        new_data.append(item)

img.putdata(new_data)

# 3. Resize to 288x384 (96x96 per tile)
# Current image might be 512x512 or something else, but we force 288x384
final_img = img.resize((288, 384), Image.Resampling.LANCZOS)

# 4. Save
final_img.save(output_path)
print(f"Successfully processed Chroma Key sprite and saved to {output_path}")
