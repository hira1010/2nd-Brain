from PIL import Image, ImageDraw
import os

img_path = 'c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作/img/characters/$Heroine.png'
out_path = 'c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作/img/characters/$Heroine.png'

if not os.path.exists(img_path):
    print(f"File not found: {img_path}")
    exit(1)

# 1. Load Original (1024x1024)
img = Image.open(img_path).convert('RGBA')
width, height = img.size
print(f"Original Size: {width}x{height}")

# 2. Add Alpha Mask
# Corner-based Flood Fill to remove checkerboard
# Use ImageDraw.floodfill(image, xy, value, thresh=0)
mask = Image.new('L', (width, height), 255)

# Fill corners with 0 (transparent)
# Thresh is 30 to catch variations in the gray checkerboard
ImageDraw.floodfill(mask, (0, 0), 0, thresh=30)
ImageDraw.floodfill(mask, (width-1, 0), 0, thresh=30)
ImageDraw.floodfill(mask, (0, height-1), 0, thresh=30)
ImageDraw.floodfill(mask, (width-1, height-1), 0, thresh=30)

# Apply mask to image alpha
img.putalpha(mask)

# 3. Resize to manageable size for RM MZ
# Total width: 288 (3 columns x 96), Total height: 384 (4 rows x 96)
# This makes her a "Large Character" (2x2 tiles)
new_size = (288, 384)
img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

# 4. Save
img_resized.save(out_path)
print(f"Fixed sprite saved to {out_path} (Size: {new_size})")
