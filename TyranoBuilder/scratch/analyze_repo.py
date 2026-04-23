import os
import sys

def get_size(start_path='.'):
    total_size = 0
    large_files = []
    folder_sizes = {}
    
    for dirpath, dirnames, filenames in os.walk(start_path):
        if '.git' in dirnames:
            dirnames.remove('.git')  # Skip git dir for content size
            
        current_folder_size = 0
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                # skip if it is a symbolic link
                if not os.path.islink(fp):
                    size = os.path.getsize(fp)
                    current_folder_size += size
                    if size > 50 * 1024 * 1024:  # > 50MB
                        large_files.append((fp, size))
            except OSError:
                continue
        
        # Track top level folders
        rel_path = os.path.relpath(dirpath, start_path)
        top_folder = rel_path.split(os.sep)[0]
        if top_folder != '.':
            folder_sizes[top_folder] = folder_sizes.get(top_folder, 0) + current_folder_size
            
        total_size += current_folder_size
        
    return total_size, large_files, folder_sizes

def main():
    root = '.'
    print(f"Analyzing {os.path.abspath(root)}...")
    total, large, folders = get_size(root)
    
    print(f"\nTotal Content Size: {total / (1024**3):.2f} GB")
    
    print("\nTop Level Folders:")
    for name, size in sorted(folders.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {size / (1024**2):.2f} MB")
        
    print("\nLarge Files (>50MB):")
    if not large:
        print("  None")
    for fp, size in sorted(large, key=lambda x: x[1], reverse=True):
        print(f"  {fp}: {size / (1024**2):.2f} MB")

if __name__ == '__main__':
    main()
