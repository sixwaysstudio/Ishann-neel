"""
Thumbnail Generator for Progressive Image Loading
Generates tiny blurred placeholder images (LQIP) for all WebP images.
"""

import os
import json
from PIL import Image, ImageFilter
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
THUMB_MAX_DIM = 40  # Max dimension (width or height) for thumbnails
THUMB_QUALITY = 60  # WebP quality (lower = smaller file)
BLUR_RADIUS = 2     # Blur radius for placeholder effect

def get_image_dimensions(img_path):
    """Get original image dimensions."""
    try:
        with Image.open(img_path) as img:
            return img.size  # (width, height)
    except Exception as e:
        print(f"Error getting dimensions for {img_path}: {e}")
        return (0, 0)

def generate_thumbnail(img_path, thumb_dir):
    """Generate a single thumbnail."""
    try:
        filename = os.path.basename(img_path)
        thumb_path = os.path.join(thumb_dir, filename)
        
        # Skip if thumbnail already exists and is newer
        if os.path.exists(thumb_path):
            if os.path.getmtime(thumb_path) >= os.path.getmtime(img_path):
                with Image.open(img_path) as img:
                    return {
                        'original': img_path,
                        'thumb': thumb_path,
                        'width': img.size[0],
                        'height': img.size[1],
                        'status': 'skipped'
                    }
        
        with Image.open(img_path) as img:
            original_width, original_height = img.size
            
            # Calculate thumbnail dimensions maintaining aspect ratio
            if original_width > original_height:
                thumb_width = THUMB_MAX_DIM
                thumb_height = int(original_height * (THUMB_MAX_DIM / original_width))
            else:
                thumb_height = THUMB_MAX_DIM
                thumb_width = int(original_width * (THUMB_MAX_DIM / original_height))
            
            # Ensure minimum dimensions
            thumb_width = max(thumb_width, 1)
            thumb_height = max(thumb_height, 1)
            
            # Resize and blur
            thumb = img.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            thumb = thumb.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
            
            # Ensure thumb directory exists
            os.makedirs(thumb_dir, exist_ok=True)
            
            # Save as WebP
            thumb.save(thumb_path, 'WEBP', quality=THUMB_QUALITY)
            
            thumb_size = os.path.getsize(thumb_path)
            
            return {
                'original': img_path,
                'thumb': thumb_path,
                'width': original_width,
                'height': original_height,
                'thumb_size': thumb_size,
                'status': 'created'
            }
            
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return {
            'original': img_path,
            'error': str(e),
            'status': 'error'
        }

def process_directory(images_dir):
    """Process all WebP images in the directory tree."""
    results = []
    tasks = []
    
    # Collect all WebP files
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith('.webp'):
                # Skip files already in thumbs directories
                if 'thumbs' in root.split(os.sep):
                    continue
                    
                img_path = os.path.join(root, file)
                thumb_dir = os.path.join(root, 'thumbs')
                tasks.append((img_path, thumb_dir))
    
    print(f"Found {len(tasks)} images to process")
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(generate_thumbnail, img, thumb_dir): (img, thumb_dir) 
                   for img, thumb_dir in tasks}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result.get('status') == 'created':
                size_kb = result.get('thumb_size', 0) / 1024
                print(f"✓ Created: {os.path.basename(result['original'])} ({size_kb:.1f}KB)")
            elif result.get('status') == 'skipped':
                print(f"○ Skipped: {os.path.basename(result['original'])} (up to date)")
            else:
                print(f"✗ Error: {os.path.basename(result['original'])}")
    
    return results

def generate_dimensions_json(results, output_path):
    """Generate a JSON file mapping image paths to dimensions."""
    dimensions = {}
    
    for result in results:
        if result.get('width') and result.get('height'):
            # Create relative path from assets folder
            original = result['original']
            # Normalize path separators
            rel_path = original.replace('\\', '/')
            if 'assets/images/' in rel_path:
                rel_path = rel_path.split('assets/images/')[1]
            
            dimensions[rel_path] = {
                'width': result['width'],
                'height': result['height']
            }
    
    with open(output_path, 'w') as f:
        json.dump(dimensions, f, indent=2)
    
    print(f"\nDimensions saved to: {output_path}")

def main():
    # Get the assets/images directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    images_dir = os.path.join(project_dir, 'assets', 'images')
    
    print("=" * 50)
    print("THUMBNAIL GENERATOR FOR PROGRESSIVE LOADING")
    print("=" * 50)
    print(f"\nScanning: {images_dir}")
    print(f"Thumbnail size: {THUMB_MAX_DIM}px max, quality {THUMB_QUALITY}%\n")
    
    # Process all images
    results = process_directory(images_dir)
    
    # Generate dimensions JSON
    dimensions_path = os.path.join(project_dir, 'assets', 'js', 'image-dimensions.json')
    generate_dimensions_json(results, dimensions_path)
    
    # Summary
    created = sum(1 for r in results if r.get('status') == 'created')
    skipped = sum(1 for r in results if r.get('status') == 'skipped')
    errors = sum(1 for r in results if r.get('status') == 'error')
    
    total_thumb_size = sum(r.get('thumb_size', 0) for r in results if r.get('thumb_size'))
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")
    print(f"Errors:  {errors}")
    print(f"Total thumbnail size: {total_thumb_size / 1024:.1f} KB")
    print("\nDone! Run generate_gallery.py to update gallery data.")

if __name__ == "__main__":
    main()
