from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Create an image with a solid color
    img = Image.new('RGB', (1280, 720), color = (73, 109, 137))
    
    # Initialize Draw
    d = ImageDraw.Draw(img)
    
    # Save the image
    img.save(path)
    print(f"Created placeholder at {path}")

if __name__ == "__main__":
    create_placeholder(r"c:\Users\hirak\Desktop\2nd-Brain\18_システム\remotion-project\public\jimi_source.jpg")
