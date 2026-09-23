import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

try:
    # البحث عن أول ملف متاح بدل إنشاء ملف جديد
    available_files = client.openall()
    if available_files:
        sheet = available_files[0]
        worksheet = sheet.get_worksheet(0)
        headers = ["التاريخ", "البيان", "المبلغ (USDT)", "الحالة", "ملاحظات"]
        worksheet.insert_row(headers, 1)
        print(f"\n✅ تم تفعيل النظام بنجاح على الملف الموجود: {sheet.title}")
        print(f"الرابط: https://docs.google.com/spreadsheets/d/{sheet.id}")
    else:
        print("\n❌ لا يوجد ملفات متاحة، يرجى إفراغ مساحة في Google Drive أولاً.")
except Exception as e:
    print(f"❌ خطأ: {e}")
