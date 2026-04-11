from PIL import Image
import os

img_path = 'c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作/img/characters/Heroine.png'
out_path = 'c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作/img/characters/$Heroine.png'

if not os.path.exists(img_path):
    print(f"File not found: {img_path}")
    # If already renamed, we are done
    if os.path.exists(out_path):
        print("Already renamed.")
        exit(0)
    exit(1)

img = Image.open(img_path).convert('RGBA')
data = img.getdata()
new_data = []

# Checkerboard: usually near white (255,255,255) and near gray (200,200,200)
for item in data:
    # If the pixel is close to a neutral gray/white (checkerboard representation)
    r, g, b, a = item
    if r > 150 and g > 150 and b > 150 and abs(r-g) < 15 and abs(g-b) < 15:
        new_data.append((0, 0, 0, 0)) # Fully transparent
    else:
        new_data.append(item)

img.putdata(new_data)
img.save(out_path)
os.remove(img_path)
print("Done fixing sprite transparency and naming.")
