import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# استيراد وظائف الأرشفة التي كتبناها سابقاً في mubariz_pro
from mubariz_pro import connect_to_sheet, scan_invoice, archive_data

# المسارات في جوالك
WATCH_DIR = "/sdcard/Mubariz_Scan/"
ARCHIVE_DIR = "/sdcard/Mubariz_Archive/"

class MubarizHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"📸 تم اكتشاف فاتورة جديدة: {event.src_path}")
            time.sleep(2) # انتظار اكتمال حفظ الصورة
            
            # 1. الاتصال بالجوجل شيت
            sheet = connect_to_sheet()
            if sheet:
                # 2. فحص الصورة واستخراج البيانات
                company, info = scan_invoice(event.src_path)
                
                # 3. الأرشفة في الجدول
                archive_data(sheet, company, info)
                
                # 4. نقل الصورة لمجلد الأرشيف لعدم تكرارها
                file_name = os.path.basename(event.src_path)
                shutil.move(event.src_path, os.path.join(ARCHIVE_DIR, file_name))
                print(f"✅ تمت الأرشفة بنجاح ونُقلت الصورة إلى المجلد النهائي.")

if __name__ == "__main__":
    # تأكد من وجود المجلدات
    os.makedirs(WATCH_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    event_handler = MubarizHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    
    print(f"🚀 نظام المبرزي يراقب الآن مجلد {WATCH_DIR}...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
