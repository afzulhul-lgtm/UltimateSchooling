"""
generate_index.py
=================
Run this script every time you add new articles.
It reads data.json and injects static HTML article links into index.html
so that Google can index all your articles without needing JavaScript.

HOW TO RUN:
    python generate_index.py

WHAT IT DOES:
    - Reads articles/data.json
    - Injects static article links into index.html (inside #seo-articles-ul)
    - Google can now read and index all your articles
    - Users still see the normal JS card layout (static list is hidden by JS)
    
ULTIMATE SCHOOLING VERSION
"""

import os
import json
import re

# ---- CHANGE THIS PATH TO MATCH YOUR COMPUTER ----
WEBSITE_ROOT = r"C:\Users\abdul\OneDrive\Desktop\Ultimate-Schooling-Web"
# --------------------------------------------------

SITE_URL = "https://ultimateschooling.com"
DATA_JSON = os.path.join(WEBSITE_ROOT, "articles", "data.json")
INDEX_HTML = os.path.join(WEBSITE_ROOT, "index.html")

print("=" * 60)
print("💻 Ultimate Schooling - Static Article Generator")
print("=" * 60)
print()
print(f"📂 Website Root: {WEBSITE_ROOT}")
print(f"📄 Data JSON: {DATA_JSON}")
print(f"🌐 Index HTML: {INDEX_HTML}")
print(f"🔗 Site URL: {SITE_URL}")
print()

# Check if data.json exists
if not os.path.exists(DATA_JSON):
    print(f"❌ ERROR: data.json not found at {DATA_JSON}")
    print("Please make sure the articles/data.json file exists.")
    exit(1)

print("📖 Reading data.json...")

with open(DATA_JSON, "r", encoding="utf-8") as f:
    articles = json.load(f)

# Sort by ID (newest first)
articles.sort(key=lambda x: int(x.get("id", 0)), reverse=True)
print(f"✅ Found {len(articles)} articles")

# Build static HTML list items
items_html = ""
categories_count = {}

for art in articles:
    title   = art.get("title", "").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    fname   = art.get("filename", "")
    excerpt = (art.get("excerpt") or "")[:120].replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    date    = art.get("date", "")
    image   = art.get("image", "")
    category = art.get("category", "Uncategorized")
    
    # Count categories for statistics
    categories_count[category] = categories_count.get(category, 0) + 1
    
    if image and not image.startswith("http"):
        image = f"articles/{image}"
    url = f"{SITE_URL}/articles/{fname}"

    items_html += f"""                <li>
                    <a href="{url}">
                        <img src="{image}" alt="{title}" loading="lazy" width="400" height="225">
                        <div>
                            <h3>{title}</h3>
                            <p>{excerpt} &mdash; <small>{date}</small></p>
                        </div>
                    </a>
                </li>\n"""

print(f"📝 Built static HTML for {len(articles)} articles")
print()
print("📊 Category Statistics:")
for cat, count in sorted(categories_count.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"   - {cat}: {count} articles")

# Check if index.html exists
if not os.path.exists(INDEX_HTML):
    print(f"\n❌ ERROR: index.html not found at {INDEX_HTML}")
    exit(1)

# Read index.html
print(f"\n📄 Reading index.html...")
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the placeholder section
start_marker = "<!-- ARTICLES_PLACEHOLDER -->"
end_marker   = "<!-- generate_index.py fills this automatically -->"

if start_marker in html and end_marker in html:
    before = html[:html.index(start_marker)]
    after  = html[html.index(end_marker) + len(end_marker):]
    new_html = before + "<!-- ARTICLES_PLACEHOLDER -->\n" + items_html + "                " + end_marker + after
    
    # Backup original file
    backup_path = INDEX_HTML + ".backup"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"💾 Backup created: index.html.backup")
    
    # Write updated file
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(new_html)
    
    print(f"\n✅ SUCCESS! index.html updated — {len(articles)} articles injected for Google")
    print(f"   File size: {len(new_html):,} bytes")
    
else:
    print("\n❌ ERROR: Placeholder markers not found in index.html")
    print("Make sure your index.html contains:")
    print("  <!-- ARTICLES_PLACEHOLDER -->")
    print("  <!-- generate_index.py fills this automatically -->")
    exit(1)

print("\n" + "=" * 60)
print("📋 NEXT STEPS FOR ULTIMATE SCHOOLING:")
print("=" * 60)
print()
print("1️⃣  Upload the updated index.html to your website")
print("   └─ File location: Ultimate-Schooling-Web/index.html")
print()
print("2️⃣  Go to Google Search Console")
print("   └─ URL Inspection > https://ultimateschooling.com/")
print("   └─ Click 'Request Indexing'")
print()
print("3️⃣  Resubmit your sitemap")
print("   └─ Sitemaps > https://ultimateschooling.com/sitemap.xml")
print("   └─ Click 'Resubmit'")
print()
print("4️⃣  Check Google Rich Results Test")
print("   └─ https://search.google.com/test/rich-results")
print("   └─ Enter: https://ultimateschooling.com/")
print()
print("💡 TIP: Run this script again every time you publish new articles.")
print("=" * 60)

print("\n✅ Ultimate Schooling SEO Generator Complete! 🚀")