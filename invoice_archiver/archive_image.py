import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import os

# إعداد الصلاحيات للـ Sheets و Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# استخدام نفس ملف المفتاح الموجود في vault
creds = ServiceAccountCredentials.from_json_keyfile_name('vault/service_account.json', scope)

# تهيئة الـ Google Sheets
client_sheets = gspread.authorize(creds)
sheet_url = "https://docs.google.com/spreadsheets/d/1MH-Q6xIYRmctyN9v3gINP4a7HkS_lGoKzqWB_y5rUsk/edit"
spreadsheet = client_sheets.open_by_url(sheet_url)
sheet = spreadsheet.get_worksheet(0)

# تهيئة الـ Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

def main():
    print("--- نظام أرشفة الفواتير المصورة من المبرزي ---")
    
    # 1. التقاط الصورة (بافتراض أنك وضعتها في مجلد الصور أو التنزيلات باسم invoice.jpg)
    # ملاحظة: Termux لا يستطيع فتح الكاميرا مباشرة بسهولة، سنعتمد على نقل الصورة
    image_path = "/storage/emulated/0/Download/invoice.jpg" # مسار الصورة في التنزيلات
    
    if not os.path.exists(image_path):
        print("❌ خطأ: لم يتم العثور على الصورة في مجلد التنزيلات باسم invoice.jpg")
        return

    code = input("أدخل رقم كود العميل: ")
    date_now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    print("\n⏳ جاري رفع الصورة إلى Google Drive...")
    
    # 2. إعداد بيانات الرفع لـ Google Drive
    file_metadata = {
        'name': f'invoice_{code}_{date_now}.jpg',
        'parents': ['root'] # سيتم الرفع للمجلد الرئيسي لـ Drive
    }
    media = MediaFileUpload(image_path, mimetype='image/jpeg')
    
    try:
        # رفع الصورة
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        file_link = file.get('webViewLink')
        print(f"✅ تم رفع الصورة لـ Drive بنجاح.")
        
        # 3. أرشفة البيانات مع الرابط في Google Sheets
        row = [date_now, code, "صورة فاتورة", file_link]
        sheet.append_row(row)
        print(f"✅ تم أرشفة البيانات مع رابط الصورة في Google Sheets!")
        
    except Exception as e:
        print(f"\n❌ فشل العملية: {e}")

if __name__ == "__main__":
    main()
