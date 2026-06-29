import os
import shutil

src_dir = r"C:\Users\hirak\Pictures\Screenshots"
dest_dir = r"c:\Users\hirak\Desktop\2nd-Brain\02_Remotion\my-video\public\images"

os.makedirs(dest_dir, exist_ok=True)

# Clear existing images
for f in os.listdir(dest_dir):
    os.remove(os.path.join(dest_dir, f))

# Get large pngs
files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith('.png')]
files = [f for f in files if os.path.getsize(f) > 50000]

# Sort by modified time (newest first)
files.sort(key=os.path.getmtime, reverse=True)

# Take top 15
top_files = files[:15]

# Copy and rename
for i, f in enumerate(top_files):
    shutil.copy2(f, os.path.join(dest_dir, f"img_{i}.png"))
    print(f"Copied {f} to img_{i}.png")

print(f"Copied {len(top_files)} images successfully.")
