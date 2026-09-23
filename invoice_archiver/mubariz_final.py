import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعداد الاتصال
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# 2. معرف الملف الذي استخرجناه من الرابط
SHEET_ID = "1ZZ0OaS0Glb42JZLVn0vCCqsoNAiR-uIlf12bzdvdsK4" 

try:
    spreadsheet = client.open_by_key(SHEET_ID)
    sheet = spreadsheet.sheet1
    
    # تنظيف الجدول من وسوم HTML وإعداد رؤوس الأعمدة
    sheet.clear()
    headers = ["م", "اسم المريض", "رقم بطاقة التأمين", "إجمالي الكلفة", "نسبة التحمل", "الخصم الإضافي", "صافي المطالبة", "رقم الكود", "التاريخ"]
    sheet.insert_row(headers, 1)
    
    # إضافة البيانات المحاسبية بدقة (بناءً على الكشوفات السابقة)
    data_to_add = [
        [1, "افكار مرشد احمد الذماري", "239*189504", 20000, 4000, 6000, 10000, "1478491", "2026-05-01"],
        [2, "نرجس يحيى درا", "309608*301", 25000, 5000, 7500, 12500, "1475446", "2026-05-01"],
        [3, "سميه علي علي", "37*166591", 20000, 0, 6000, 14000, "1479043", "2026-05-01"]
    ]
    
    for row in data_to_add:
        sheet.append_row(row)
        
    print("✅ تم بنجاح: تنظيف الجدول وإعداد التقرير المحاسبي لمركز المبرزي.")

except Exception as e:
    print(f"❌ خطأ: تأكد من مشاركة الملف مع البريد الإلكتروني الخاص بـ Service Account.")
