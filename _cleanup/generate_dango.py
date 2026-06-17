import os

filepath = r"C:\Users\hirak\Desktop\2nd-Brain\DangoShop.obj"
mtl_path = r"C:\Users\hirak\Desktop\2nd-Brain\DangoShop.mtl"

vertices = []
materials = {}

def add_cube(x, y, z, sx, sy, sz, mat_name):
    start_v = len(vertices) + 1
    dx, dy, dz = sx / 2.0, sy / 2.0, sz / 2.0
    
    vertices.extend([
        (x - dx, y - dy, z - dz), (x + dx, y - dy, z - dz),
        (x + dx, y + dy, z - dz), (x - dx, y + dy, z - dz),
        (x - dx, y - dy, z + dz), (x + dx, y - dy, z + dz),
        (x + dx, y + dy, z + dz), (x - dx, y + dy, z + dz)
    ])
    
    faces = [
        (start_v+0, start_v+1, start_v+2, start_v+3), # Bottom
        (start_v+4, start_v+7, start_v+6, start_v+5), # Top
        (start_v+0, start_v+4, start_v+5, start_v+1), # Front
        (start_v+1, start_v+5, start_v+6, start_v+2), # Right
        (start_v+2, start_v+6, start_v+7, start_v+3), # Back
        (start_v+3, start_v+7, start_v+4, start_v+0)  # Left
    ]
    materials.setdefault(mat_name, []).extend(faces)

def add_prism(x, y, z, sx, sy, sz, mat_name):
    start_v = len(vertices) + 1
    dx, dy, dz = sx / 2.0, sy / 2.0, sz / 2.0
    
    vertices.extend([
        (x - dx, y - dy, z - dz), (x + dx, y - dy, z - dz), (x, y - dy, z + dz),
        (x - dx, y + dy, z - dz), (x + dx, y + dy, z - dz), (x, y + dy, z + dz)
    ])
    
    faces = [
        (start_v+0, start_v+1, start_v+4, start_v+3), # Bottom
        (start_v+0, start_v+3, start_v+5, start_v+2), # Left Slant
        (start_v+1, start_v+2, start_v+5, start_v+4), # Right Slant
        (start_v+0, start_v+2, start_v+1),            # Front
        (start_v+3, start_v+4, start_v+5)             # Back
    ]
    materials.setdefault(mat_name, []).extend(faces)

# Building the shop layout
add_cube(0, 0, 1, 3, 2, 2, "Wood")      # Base structure
add_prism(0, 0, 2.5, 3.5, 2.5, 1.5, "Roof") # Roof
add_cube(0, 1.05, 1.2, 2.8, 0.1, 0.8, "Cloth") # Noren curtains
add_cube(0, 1.2, 2.0, 1.5, 0.1, 0.5, "Wood") # Signboard
add_cube(-1.8, 1.2, 1.5, 0.5, 0.5, 0.8, "Lantern") # Lantern L
add_cube(1.8, 1.2, 1.5, 0.5, 0.5, 0.8, "Lantern") # Lantern R
add_cube(1.0, 1.5, 0.5, 0.8, 0.5, 0.5, "Wood") # Small table in front

# Write OBJ
with open(filepath, "w") as f:
    f.write("mtllib DangoShop.mtl\n")
    for v in vertices:
        # Swap Y and Z so it stands upright
        f.write(f"v {v[0]:.4f} {v[2]:.4f} {v[1]:.4f}\n")
    
    for mat_name, faces in materials.items():
        f.write(f"usemtl {mat_name}\n")
        for face in faces:
            f.write("f " + " ".join(str(idx) for idx in face) + "\n")

# Write MTL
with open(mtl_path, "w") as f:
    f.write("newmtl Wood\nKd 0.6 0.4 0.2\n\n")
    f.write("newmtl Roof\nKd 0.1 0.2 0.4\n\n")
    f.write("newmtl Cloth\nKd 0.8 0.1 0.1\n\n")
    f.write("newmtl Lantern\nKd 0.9 0.2 0.1\n")

print(f"Successfully generated {filepath}")
