import os
from PIL import Image

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

images = [
    "assets/images/home/sub.webp",
    "assets/images/story.webp",
    "assets/images/works/STREET/DSC00407.webp",
    "assets/images/works/WILD LIFE/_DSC0190_1.webp",
    "assets/images/works/LANDSCAPE/_DSC0041.webp",
    "assets/images/works/EXHIBITION/DSC00234 (3).webp",
    "assets/images/exhibition.webp"
]

base_dir = r"c:/Users/CHARGE/Desktop/websites/Photo Graph"

print(f"{'Image Path':<60} {'Size':<10} {'Dimensions':<15}")
print("-" * 85)

for img_rel_path in images:
    img_path = os.path.join(base_dir, img_rel_path)
    try:
        size = os.path.getsize(img_path)
        with Image.open(img_path) as img:
            dims = f"{img.width}x{img.height}"
        
        print(f"{img_rel_path:<60} {get_size_format(size):<10} {dims:<15}")
    except FileNotFoundError:
        print(f"{img_rel_path:<60} NOT FOUND")
    except Exception as e:
        print(f"{img_rel_path:<60} ERROR: {e}")
