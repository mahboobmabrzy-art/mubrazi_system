import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
SHEET_ID = "1ZZ0OaS0Glb42JZLVn0vCCqsoNAiR-uIlf12bzdvdsK4"
sheet = client.open_by_key(SHEET_ID).sheet1

# تحديث رؤوس الأعمدة لتشمل جهة التأمين
new_headers = ["م", "جهة التأمين", "اسم المريض", "رقم البطاقة", "إجمالي الكلفة", "نسبة التحمل", "الخصم", "الصافي", "رقم الكود", "التاريخ"]
sheet.update('A1:J1', [new_headers])
print("✅ تم تحديث هيكلة الجدول لتشمل جميع شركات التأمين.")
