import os
import time
from PIL import Image
import gspread
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

# --- الإعدادات الثابتة ---
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

# معرفات نظام المبرزي للبصريات
DRIVE_FOLDER_ID = 'أدخل_هنا_ID_المجلد'  # ضع ID المجلد المشترك هنا
SPREADSHEET_ID = '1MH-Q6xIYRmctyN9v3gINP4a7HkS_lGoKzqWB_y5rUsk'

def get_creds():
    return Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def compress_image(image_path):
    """تصغير حجم الصورة لتجنب انقطاع الاتصال 103"""
    print("🛠 جاري معالجة الصورة لضمان استقرار الرفع...")
    img = Image.open(image_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.thumbnail((1200, 1200))
    temp_path = "ready_to_upload.jpg"
    img.save(temp_path, "JPEG", quality=70, optimize=True)
    return temp_path

def upload_and_log(file_name):
    try:
        creds = get_creds()
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_client = gspread.authorize(creds)
        
        # 1. ضغط الصورة
        processed_file = compress_image(file_name)
        
        # 2. الرفع إلى Google Drive (مع ميزة الاستئناف Resumable)
        file_metadata = {
            'name': f"Invoice_{int(time.time())}.jpg",
            'parents': [DRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(processed_file, mimetype='image/jpeg', resumable=True)
        
        print("🚀 بدء الرفع إلى Drive...")
        request = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink')
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"📡 تقدم الرفع: {int(status.progress() * 100)}%")

        file_id = response.get('id')
        file_link = response.get('webViewLink')
        print(f"✅ تم الرفع بنجاح. ID: {file_id}")

        # 3. التدوين في Google Sheets (الملف الذي أرسلته)
        sheet = sheets_client.open_by_key(SPREADSHEET_ID).sheet1
        log_data = [
            time.strftime("%Y-%m-%d %H:%M:%S"), # التاريخ والوقت
            "فاتورة بصرية/سمعية",                # النوع
            file_link,                          # رابط الصورة
            "قيد المعالجة"                       # الحالة
        ]
        sheet.append_row(log_data)
        print("📊 تم تسجيل البيانات في الجدول بنجاح.")

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    # تأكد من وجود ملف بهذا الاسم في المجلد للتجربة
    # يمكنك تغيير 'image.png' لاسم أي صورة عندك
    target_image = 'image.png' 
    if os.path.exists(target_image):
        upload_and_log(target_image)
    else:
        print(f"⚠️ الملف {target_image} غير موجود في المجلد الحالي.")
