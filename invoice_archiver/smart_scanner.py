import pytesseract
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime

# 1. إعداد الاتصال بجوجل شيت
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
SHEET_ID = "1ZZ0OaS0Glb42JZLVn0vCCqsoNAiR-uIlf12bzdvdsK4"
sheet = client.open_by_key(SHEET_ID).sheet1

def scan_and_archive(image_path):
    print(f"🔍 جاري معالجة الصورة: {image_path}...")
    
    try:
        # 2. قراءة النص باستخدام محرك OCR
        # ملاحظة: تأكد من تثبيت tesseract-lang-ara في Termux
        raw_text = pytesseract.image_to_string(Image.open(image_path), lang='ara')
        
        # 3. محرك التصنيف الذكي (تحديد الشركة)
        company = "عميل نقدي"
        if "كاك" in raw_text: company = "كاك للتأمين"
        elif "المتحدة" in raw_text: company = "المتحدة للتأمين"
        elif "اليمنية" in raw_text: company = "اليمنية للتأمين"
        elif "المخصصة" in raw_text: company = "المخصصة للتأمين"
        elif "الحياة" in raw_text: company = "الحياة للتأمين"
        elif "المبرزي" in raw_text: company = "مركز المبرزي"

        # 4. استخراج الأرقام (مثل رقم البطاقة أو المبلغ)
        # سنبحث عن أول سلسلة أرقام طويلة كافتراض لرقم البطاقة
        numbers = re.findall(r"\d+", raw_text)
        card_no = numbers[0] if numbers else "غير موجود"
        
        # 5. تجهيز البيانات للأرشفة
        next_id = len(sheet.get_all_values())
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # الصف المراد إضافته
        row = [next_id, company, "جاري التحقق..", card_no, 0, 0, 0, 0, "الماسح الذكي", date_str]
        
        sheet.append_row(row)
        print(f"✅ تم بنجاح تصنيف العميل كـ: [{company}] وإضافته للجدول.")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")

# لفتح الكاميرا أو معالجة ملف معين، استدعي الدالة هنا:
# scan_and_archive('test_image.jpg')
