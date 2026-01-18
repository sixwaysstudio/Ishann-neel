import os
from PIL import Image

def convert_to_webp(root_dir):
    extensions = ('.jpg', '.jpeg', '.png')
    
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            filename, ext = os.path.splitext(file)
            
            if ext.lower() in extensions:
                try:
                    with Image.open(file_path) as img:
                        webp_path = os.path.join(subdir, f"{filename}.webp")
                        print(f"Converting: {file_path} -> {webp_path}")
                        img.save(webp_path, "WEBP", quality=85)
                    
                    # Delete original file
                    os.remove(file_path)
                    print(f"Deleted original: {file_path}")
                except Exception as e:
                    print(f"Error converting {file_path}: {e}")

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images")
    print(f"Scanning directory: {assets_dir}")
    convert_to_webp(assets_dir)
    print("Conversion complete.")
