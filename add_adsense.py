import os

# 1. Apna asli AdSense code yahan paste karen (triple quotes ke andar)
ADSENSE_CODE = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>"""

def inject_adsense_to_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Check karna ke kahin code pehle se toh maujood nahi
    if "googlesyndication.com/pagead/js/adsbygoogle.js" in content:
        print(self_marker := f"Skipped (Already exists): {file_path}")
        return

    # <head> tag ke thora niche code ko insert karna
    if "<head>" in content:
        # <head> ke foran baad code aur new line add kar rahe hain
        modified_content = content.replace("<head>", f"<head>\n    {ADSENSE_CODE}")
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"Successfully Added: {file_path}")
    else:
        print(f"Warning (No <head> tag found): {file_path}")

def process_all_folders(root_dir):
    # os.walk poore root aur subfolders ki html files ko check karega
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                inject_adsense_to_html(file_path)

if __name__ == "__main__":
    # '.' ka matlab hai current folder jahan script pari hui hai
    current_directory = '.' 
    print("Starting AdSense code injection...")
    process_all_folders(current_directory)
    print("Process completed!")