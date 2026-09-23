import os
import shutil
import hashlib

SOURCE = "/sdcard/Download"
DESTINATION = "/sdcard/My_Empire"

STRUCTURE = {
    "01_Programming": [".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".php", ".ts"],
    "02_Marketing_Ads": [".jpg", ".jpeg", ".png", ".mp4", ".pdf", ".docx", ".txt", ".pptx"],
    "03_Database_Assets": [".db", ".sql", ".xml", ".env", ".key"],
    "04_Archive_Old": [".zip", ".rar", ".tar", ".gz"]
}

def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except: return None

def main():
    print("\n[+] Running Organization...")
    if not os.path.exists(DESTINATION): os.makedirs(DESTINATION)
    hashes, moved, deleted = {}, 0, 0
    for root, dirs, files in os.walk(SOURCE):
        for file in files:
            path = os.path.join(root, file)
            if not os.path.isfile(path): continue
            if os.path.getsize(path) < 5: continue
            f_hash = get_file_hash(path)
            if f_hash and f_hash in hashes:
                os.remove(path)
                deleted += 1
                continue
            hashes[f_hash] = path
            ext = os.path.splitext(file)[1].lower()
            is_moved = False
            for folder, extensions in STRUCTURE.items():
                if ext in extensions:
                    target_path = os.path.join(DESTINATION, folder)
                    os.makedirs(target_path, exist_ok=True)
                    shutil.move(path, os.path.join(target_path, file))
                    moved += 1
                    is_moved = True
                    break
            if not is_moved:
                others = os.path.join(DESTINATION, "05_Unclassified")
                os.makedirs(others, exist_ok=True)
                shutil.move(path, os.path.join(others, file))
    print(f"\nDone! Moved: {moved} | Deleted: {deleted}")

if __name__ == "__main__":
    main()

