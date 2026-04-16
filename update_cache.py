import os
import glob
import re

# 🔴 Jab bhi aap mustaqbil (future) mein koi Design/JS change karein, toh bas is number ko badal dein (e.g., 5.0, 6.0)
NEW_VERSION = "4.0"

# Anti-Cache Tags (Jo browser ko purani file save karne se rokte hain)
CACHE_TAGS = """
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
"""

# Current folder aur articles folder dono ki HTML files uthao
html_files = glob.glob("*.html") + glob.glob("articles/*.html")

print(f"🔄 Total {len(html_files)} files update ho rahi hain (Version {NEW_VERSION})...")
print("💻 Ultimate Schooling - Cache Update System")
print("=" * 50)

updated_count = 0
error_count = 0

for file_path in html_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = False

        # 1. CSS aur JS ka version update karo
        if re.search(r'style\.css\?v=[\d\.]+', content):
            content = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={NEW_VERSION}', content)
            changes_made = True
        
        if re.search(r'script\.js\?v=[\d\.]+', content):
            content = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={NEW_VERSION}', content)
            changes_made = True

        # 2. Agar Meta Tags nahi lage toh laga do
        if "Cache-Control" not in content and "</head>" in content:
            content = content.replace("</head>", f"{CACHE_TAGS}\n</head>")
            changes_made = True

        # 3. Sirf tabhi write karo jab changes hue hon
        if changes_made and content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            updated_count += 1
            print(f"  ✅ Updated: {file_path}")
            
    except Exception as e:
        error_count += 1
        print(f"  ❌ Error in {file_path}: {e}")

print("=" * 50)
print(f"✅ Ultimate Schooling Cache System Update Complete!")
print(f"📊 Statistics:")
print(f"   - Total Files Scanned: {len(html_files)}")
print(f"   - Files Updated: {updated_count}")
print(f"   - Errors: {error_count}")
print(f"   - New Version: v{NEW_VERSION}")
print()
print("💡 Next Steps:")
print("   1. Ab aap apna code GitHub Desktop se Push kar sakte hain")
print("   2. Visitors ko fresh version milega - no more cache issues! 🚀")