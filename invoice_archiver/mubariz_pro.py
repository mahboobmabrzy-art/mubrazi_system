import pytesseract
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime

# 1. إعدادات الاتصال والوصول (نظام المبرزي)
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        # المعرف الخاص بملفك الذي استخرجناه سابقاً
        SHEET_ID = "1ZZ0OaS0Glb42JZLVn0vCCqsoNAiR-uIlf12bzdvdsK4"
        return client.open_by_key(SHEET_ID).sheet1
    except Exception as e:
        print(f"❌ خطأ في الاتصال بجوجل شيت: {e}")
        return None

# 2. محرك الفحص والتعرف الذكي (OCR & Classification)
def scan_invoice(image_path):
    print(f"🔍 جاري تحليل الصورة: {image_path}...")
    try:
        # قراءة النص من الصورة (دعم العربية)
        raw_text = pytesseract.image_to_string(Image.open(image_path), lang='ara')
        
        # تحديد شركة التأمين بناءً على الكلمات المفتاحية
        company = "مركز المبرزي (نقدي)"
        if "كاك" in raw_text: company = "كاك للتأمين"
        elif "المتحدة" in raw_text: company = "المتحدة للتأمين"
        elif "اليمنية" in raw_text: company = "اليمنية للتأمين"
        elif "المخصصة" in raw_text: company = "المخصصة للتأمين"
        elif "الحياة" in raw_text: company = "الحياة للتأمين"
        
        # استخراج الأرقام (رقم البطاقة أو المبلغ)
        numbers = re.findall(r"\d+", raw_text)
        card_or_amount = numbers[0] if numbers else "0"
        
        return company, card_or_amount
    except Exception as e:
        print(f"❌ خطأ في قراءة الصورة: {e}")
        return "خطأ", "0"

# 3. الأرشفة النهائية وتحديث الجدول
def archive_data(sheet, company, info):
    try:
        # الحصول على رقم الصف التالي
        next_id = len(sheet.get_all_values())
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # الصف المحاسبي المتكامل
        # [م، جهة التأمين، اسم المريض، رقم البطاقة، التكلفة، التحمل، الخصم، الصافي، الكود، التاريخ]
        row = [next_id, company, "مستخرج آلياً", info, 0, 0, 0, 0, "الماسح الذكي", date_now]
        
        sheet.append_row(row)
        print(f"✅ تمت الأرشفة بنجاح: {company} | بيانات: {info}")
    except Exception as e:
        print(f"❌ خطأ أثناء الأرشفة: {e}")

# --- تشغيل النظام ---
if __name__ == "__main__":
    mubariz_sheet = connect_to_sheet()
    if mubariz_sheet:
        # البدء بمعالجة الفاتورة التي سميناها invoice.jpg
        company_name, extracted_info = scan_invoice('invoice.jpg')
        archive_data(mubariz_sheet, company_name, extracted_info)

