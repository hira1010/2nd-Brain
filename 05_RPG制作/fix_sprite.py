import os
from PIL import Image, ImageEnhance
import random

src_path = "img/characters/$Actor1_new.png"
dst_path = "img/characters/$Actor1_damaged.png"

try:
    img = Image.open(src_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for r, g, b, a in data:
        if a > 0:
            factor = random.uniform(0.6, 0.9)
            new_r = min(255, int(r * factor + random.randint(0, 30)))
            new_g = int(g * factor * 0.9)
            new_b = int(b * factor * 0.9)
            new_data.append((new_r, new_g, new_b, a))
        else:
            new_data.append((r, g, b, a))
            
    img.putdata(new_data)
    
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.7)
    
    img.save(dst_path)
    print("Success: Sprite successfully regenerated.")
except Exception as e:
    print(f"Error: {e}")
