import os
from PIL import Image

def optimize_webp_images(root_dir, max_size_mb=0.5, max_dimension=1920, quality=80):
    print(f"Starting optimization in: {root_dir}")
    print(f"Target: < {max_size_mb}MB, Max Dim: {max_dimension}px, Quality: {quality}")
    
    total_saved = 0
    count = 0
    
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.webp'):
                file_path = os.path.join(subdir, file)
                try:
                    size_bytes = os.path.getsize(file_path)
                    size_mb = size_bytes / (1024 * 1024)
                    
                    # Only optimize if larger than threshold or just generally large (e.g. > 500KB)
                    # The prompt asked to decrease file size, so let's be aggressive but safe
                    if size_mb > max_size_mb:
                        with Image.open(file_path) as img:
                            # Check dimensions
                            width, height = img.size
                            if width > max_dimension or height > max_dimension:
                                # Calculate new dimensions
                                if width > height:
                                    new_width = max_dimension
                                    new_height = int(height * (max_dimension / width))
                                else:
                                    new_height = max_dimension
                                    new_width = int(width * (max_dimension / height))
                                
                                print(f"Resizing {file}: {width}x{height} -> {new_width}x{new_height}")
                                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            
                            # Save optimized
                            img.save(file_path, 'WEBP', quality=quality)
                            
                            new_size_bytes = os.path.getsize(file_path)
                            saved = size_bytes - new_size_bytes
                            total_saved += saved
                            count += 1
                            
                            print(f"Optimized {file}: {size_mb:.2f}MB -> {new_size_bytes/(1024*1024):.2f}MB (Saved: {saved/(1024*1024):.2f}MB)")
                            
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"\nOptimization Complete.")
    print(f"Processed {count} images.")
    print(f"Total space saved: {total_saved / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images")
    optimize_webp_images(assets_dir)
