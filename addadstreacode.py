import os

# Adsterra ka Social Bar code jo aapne diya hai
ad_code = '<script src="https://pl30375253.effectivecpmnetwork.com/d7/70/66/d7706649f4c79443f23285bd367a6ed1.js"></script>'

# Current directory (jahan script run hoga)
root_dir = '.'

count = 0

print("🔍 Scanning HTML files and injecting Adsterra code...\n")

# os.walk se root folder aur uske andar ke sabhi folders check honge
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            
            # File ko read karna
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check karna ke code pehle se toh nahi laga hua (taake duplicate na ho)
            if ad_code not in content:
                # </body> tag dhoond kar us se pehle ad code lagana
                if '</body>' in content:
                    # Code ko inject karna
                    new_content = content.replace('</body>', f'{ad_code}\n</body>')
                    
                    # File ko wapis save karna
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    print(f"✅ Ad added successfully to: {filepath}")
                    count += 1
                else:
                    print(f"⚠️ Warning: </body> tag not found in {filepath} (Skipped)")
            else:
                print(f"⏭️ Skipped (Ad code already exists): {filepath}")

print(f"\n🎉 Done! Adsterra Social Bar code has been added to {count} HTML files.")