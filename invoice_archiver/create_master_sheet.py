import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

try:
    # إنشاء جدول جديد باسم المركز
    sheet = client.create('نظام المبرزي المحاسبي 2026')
    
    # مشاركة الملف مع بريدك الشخصي لتتمكن من رؤيته (اختياري)
    # sheet.share('your-email@gmail.com', perm_type='user', role='writer')
    
    worksheet = sheet.get_worksheet(0)
    # إضافة العناوين الرئيسية
    headers = ["التاريخ", "البيان", "المبلغ (USDT)", "الحالة", "ملاحظات"]
    worksheet.append_row(headers)
    
    print(f"\n✅ تم إنشاء جدول البيانات بنجاح!")
    print(f"الرابط: https://docs.google.com/spreadsheets/d/{sheet.id}")
except Exception as e:
    print(f"❌ حدث خطأ: {e}")
