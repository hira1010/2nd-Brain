import os
import shutil

root = r'C:\Users\hirak\Desktop\2nd-Brain'
src24 = os.path.join(root, '24_Pyxel')
dst20 = os.path.join(root, '20_Godot_Pyxel')
final20 = os.path.join(root, '20_Pyxel_Godot')

print(f"Moving contents from {src24} to {dst20}...")

if os.path.exists(src24) and os.path.exists(dst20):
    for item in os.listdir(src24):
        s = os.path.join(src24, item)
        d = os.path.join(dst20, item)
        
        if os.path.exists(d):
            if os.path.isdir(d):
                shutil.rmtree(d)
            else:
                os.remove(d)
        
        shutil.move(s, d)
        print(f" Moved: {item}")
    
    try:
        shutil.rmtree(src24)
        print(f"Deleted source directory: {src24}")
    except Exception as e:
        print(f"Could not delete {src24} (it might be in use): {e}")

if os.path.exists(dst20):
    if os.path.exists(final20):
        print(f"Final directory {final20} already exists. Merging into it...")
        for item in os.listdir(dst20):
            shutil.move(os.path.join(dst20, item), os.path.join(final20, item))
        os.rmdir(dst20)
    else:
        os.rename(dst20, final20)
    print(f"Integration to {final20} complete.")

print("Process finished.")
