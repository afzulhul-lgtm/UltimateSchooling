"""
add_analytics_all.py — data.json se sab articles mein Google Analytics code add karo
"""

import os
import json

ANALYTICS_CODE = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3Y5HBVKECV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-3Y5HBVKECV');
</script>'''

# ⚠️ PATHS YAHAN DAALO
ARTICLES_FOLDER = r"C:\Users\abdul\Downloads\UltimateSchooling\UltimateSchooling\articles"
DATA_JSON_FILE = os.path.join(ARTICLES_FOLDER, "data.json")

# 1. data.json se articles ki list lo
with open(DATA_JSON_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"📋 {len(articles)} articles found in data.json\n")

count = 0
skipped = 0
missing = 0

# 2. Har article ki HTML file update karo
for art in articles:
    filename = art.get("filename", "").strip()
    if not filename:
        skipped += 1
        continue
    
    filepath = os.path.join(ARTICLES_FOLDER, filename)
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"❌ File missing: {filename}")
        missing += 1
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Skip if code already exists
    if "googletagmanager.com" in content:
        skipped += 1
        continue
    
    # Add code after <head>
    if "<head>" in content:
        content = content.replace("<head>", f"<head>\n{ANALYTICS_CODE}")
    elif "<html" in content:
        content = content.replace("<html", f"<html>\n<head>\n{ANALYTICS_CODE}\n</head>", 1)
    else:
        print(f"⚠️  No <head> tag: {filename}")
        skipped += 1
        continue
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    count += 1
    print(f"✅ [{count}] {filename}")

print(f"\n{'='*55}")
print(f"🎉 Done!")
print(f"   ✅ Updated: {count} articles")
print(f"   ⏭️  Skipped: {skipped} (already done or no <head>)")
print(f"   ❌ Missing: {missing} files")
print(f"   📁 Total in data.json: {len(articles)}")
print(f"{'='*55}")