"""
Ultimate Schooling - Advanced Image Optimization Script
=======================================================
This script converts ALL image formats to WebP for maximum performance.
Supports: JPG, JPEG, PNG, GIF, BMP, TIFF, and AVIF formats.

HOW TO RUN:
    python convert_to_webp.py

WHAT IT DOES:
    - Converts all images to .webp format (25-35% smaller)
    - Updates all HTML files to reference .webp instead of original formats
    - Updates articles/data.json to use .webp extensions
    - Removes original heavy image files after conversion
    - Significantly improves page load speed for students worldwide

REQUIREMENTS:
    pip install Pillow
    (For AVIF support: pip install pillow-avif-plugin)
"""

import os
import glob
from PIL import Image

# ============================================
# CONFIGURATION
# ============================================
ARTICLES_DIR = "articles"
JSON_FILE = os.path.join(ARTICLES_DIR, "data.json")
WEBP_QUALITY = 80  # 80% quality = optimal balance between size and quality

# Statistics tracking
stats = {
    "converted": 0,
    "skipped": 0,
    "errors": 0,
    "html_updated": 0,
    "size_saved": 0,
    "formats_found": {}
}

# ============================================
# MAIN CONVERSION PROCESS
# ============================================

print("=" * 60)
print("💻 Ultimate Schooling - Advanced WebP Converter")
print("=" * 60)
print()

# Articles folder mein saari images dhoondo (including AVIF)
print("🔍 Scanning for images in articles folder...")

# All supported image formats
image_extensions = ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG", 
                    "*.png", "*.PNG", 
                    "*.gif", "*.GIF",
                    "*.bmp", "*.BMP",
                    "*.tiff", "*.tif", "*.TIFF", "*.TIF",
                    "*.avif", "*.AVIF"]

images = []
for ext in image_extensions:
    found = glob.glob(os.path.join(ARTICLES_DIR, ext))
    images.extend(found)
    if found:
        ext_clean = ext.replace("*", "").lower()
        stats["formats_found"][ext_clean] = len(found)

if not images:
    print("✅ Koi image nahi mili convert karne ke liye!")
    print("💡 Ultimate Schooling images are already optimized!")
else:
    print(f"📸 Found {len(images)} images to optimize")
    print("\n📊 Formats detected:")
    for fmt, count in stats["formats_found"].items():
        print(f"   - {fmt}: {count} files")
    
    print(f"\n🚀 Converting all images to WebP format (Quality: {WEBP_QUALITY}%)...\n")
    
    for i, img_path in enumerate(images, 1):
        try:
            # Get original file size
            original_size = os.path.getsize(img_path)
            
            # Image ko open karo (AVIF bhi support hoga agar PIL latest version hai)
            img = Image.open(img_path)
            
            # Convert RGBA/LA/P to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Naya naam banao (.webp ke sath)
            base_name = os.path.basename(img_path)
            name_without_ext = base_name.rsplit(".", 1)[0]
            webp_path = os.path.join(ARTICLES_DIR, name_without_ext + ".webp")
            
            # WebP format mein save karo
            img.save(webp_path, "webp", quality=WEBP_QUALITY, method=6)
            
            # Get new file size
            new_size = os.path.getsize(webp_path)
            size_saved = original_size - new_size
            stats["size_saved"] += size_saved
            savings_percent = (size_saved / original_size) * 100 if original_size > 0 else 0
            
            # Purani heavy file ko hamesha ke liye delete kar do
            os.remove(img_path)
            
            stats["converted"] += 1
            print(f"  ✅ [{i}/{len(images)}] {base_name} → {name_without_ext}.webp")
            print(f"      💾 Saved: {size_saved // 1024} KB ({savings_percent:.1f}% smaller)")
            
        except Exception as e:
            stats["errors"] += 1
            error_msg = str(e)
            if "AVIF" in error_msg.upper():
                print(f"  ⚠️ AVIF support not installed. Run: pip install pillow-avif-plugin")
                print(f"     Skipping: {os.path.basename(img_path)}")
            else:
                print(f"  ❌ Error converting {os.path.basename(img_path)}: {error_msg[:50]}")

    print(f"\n📊 Conversion Summary:")
    print(f"   ✅ Successfully converted: {stats['converted']} images")
    print(f"   ❌ Errors: {stats['errors']}")
    if stats["converted"] > 0:
        print(f"   💾 Total space saved: {stats['size_saved'] // 1024 // 1024} MB")
        print(f"   📈 Average savings: {(stats['size_saved'] // stats['converted']) // 1024} KB per image")

# ============================================
# UPDATE HTML FILES
# ============================================

print("\n📄 Updating HTML files to use .webp extensions...")

# File extension mapping
extensions_to_replace = [".jpg", ".jpeg", ".JPG", ".JPEG", 
                         ".png", ".PNG", 
                         ".gif", ".GIF",
                         ".bmp", ".BMP",
                         ".tiff", ".tif", ".TIFF", ".TIF",
                         ".avif", ".AVIF"]

html_files = glob.glob("*.html") + glob.glob(os.path.join(ARTICLES_DIR, "*.html"))

for html_file in html_files:
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Jahan jahan koi bhi image extension likhi hai, usay .webp kar do
        for ext in extensions_to_replace:
            content = content.replace(ext, ".webp")
        
        if content != original_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(content)
            stats["html_updated"] += 1
            print(f"  ✅ Updated: {html_file}")
            
    except Exception as e:
        print(f"  ⚠️ Could not update {html_file}: {str(e)[:30]}")

# ============================================
# UPDATE DATA.JSON
# ============================================

print("\n📊 Updating data.json references...")

if os.path.exists(JSON_FILE):
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Saare extensions ko .webp se replace karo
        for ext in extensions_to_replace:
            content = content.replace(ext, ".webp")
        
        if content != original_content:
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            print("  ✅ data.json successfully updated with .webp references!")
        else:
            print("  ℹ️ data.json already uses .webp references")
            
    except Exception as e:
        print(f"  ❌ Error updating data.json: {e}")
else:
    print(f"  ⚠️ data.json not found at {JSON_FILE}")

# ============================================
# FINAL SUMMARY
# ============================================

print("\n" + "=" * 60)
print("🎉 ULTIMATE SCHOOLING - OPTIMIZATION COMPLETE!")
print("=" * 60)
print()
print("📊 Final Statistics:")
print(f"   🖼️  Images converted: {stats['converted']}")
print(f"   📄 HTML files updated: {stats['html_updated']}")
if stats["converted"] > 0:
    print(f"   💾 Total space saved: {stats['size_saved'] // 1024 // 1024} MB")
print()
print("⚡ Benefits for Ultimate Schooling:")
print("   ✅ 25-35% smaller file sizes")
print("   ✅ Faster page loading for students worldwide")
print("   ✅ Better Google PageSpeed Insights score")
print("   ✅ Improved SEO ranking")
print("   ✅ Reduced bandwidth usage")
print("   ✅ Better mobile experience for learners")
print("   ✅ All formats unified to WebP")
print()
print("📋 NEXT STEPS:")
print("   1️⃣  Test your website locally:")
print("       - Check if images load correctly")
print("       - Verify all thumbnails appear")
print("   2️⃣  Commit changes in GitHub Desktop:")
print("       - All .webp files (new images)")
print("       - Updated .html files")
print("       - Updated articles/data.json")
print("       - Delete old .jpg/.png/.avif files from repo")
print("   3️⃣  Push to GitHub")
print("   4️⃣  Deploy to your hosting")
print()
print("💡 TIPS:")
print("   - Run this script whenever you add new images")
print("   - For AVIF support, install: pip install pillow-avif-plugin")
print("   - WebP is supported by 97%+ browsers worldwide")
print()
print("🚀 Ultimate Schooling is now running at peak performance! 💻")
print("=" * 60)