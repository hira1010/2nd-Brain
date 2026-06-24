import os
from PIL import Image, ImageDraw

def create_image(filename, size, color, text):
    img = Image.new('RGBA', size, color)
    draw = ImageDraw.Draw(img)
    # Simple text drawing (won't be perfect without a font file, but enough for placeholder)
    draw.text((10, size[1]//2 - 5), text, fill=(255,255,255,255))
    img.save(filename)

assets_dir = r"c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\Assets"
os.makedirs(assets_dir, exist_ok=True)

# Player 1 (Red)
create_image(os.path.join(assets_dir, "player1.png"), (64, 64), (200, 50, 50, 255), "P1")
# Player 2 (Blue)
create_image(os.path.join(assets_dir, "player2.png"), (64, 64), (50, 50, 200, 255), "P2")
# Ball (Yellow)
create_image(os.path.join(assets_dir, "ball.png"), (32, 32), (200, 200, 50, 255), "Ball")

print("Assets created successfully.")
