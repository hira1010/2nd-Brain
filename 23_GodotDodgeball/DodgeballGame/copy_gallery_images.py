import os
import shutil

src_dir = r"C:\Users\hirak\Desktop\特典"
dst_dir = r"c:\Users\hirak\Desktop\2nd-Brain\23_GodotDodgeball\DodgeballGame\Assets\Gallery"

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

copied = 0
for filename in sorted(os.listdir(src_dir)):
    if filename.lower().endswith('.png'):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        shutil.copy(src_path, dst_path)
        copied += 1

print(f"Copied {copied} images successfully to {dst_dir}.")
