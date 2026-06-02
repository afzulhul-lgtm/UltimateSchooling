import os

def delete_duplicate_files(root_dir):
    print("Searching for duplicate files with '(1)' in name...")
    deleted_count = 0

    # os.walk poore project aur subfolders (articles, tools wagera) ko scan karega
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Check karna ke file ke naam mein '(1).html' ya '(1)' maujood hai
            if "(1)" in file:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    print("----------------------------------------")
    print(f"Process completed! Total {deleted_count} duplicate files deleted.")

if __name__ == "__main__":
    # '.' ka matlab hai current directory jahan script pari hui hai
    current_directory = '.' 
    delete_duplicate_files(current_directory)