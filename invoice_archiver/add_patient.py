import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# إعداد الاتصال
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# معرف الجدول الخاص بك
SHEET_ID = "1ZZ0OaS0Glb42JZLVn0vCCqsoNAiR-uIlf12bzdvdsK4"
sheet = client.open_by_key(SHEET_ID).sheet1

def insert_patient_data(name, card_no, total_cost, deductible_percent, discount):
    # حسابات محاسبية تلقائية
    deductible_amount = total_cost * (deductible_percent / 100)
    net_claim = total_cost - (deductible_amount + discount)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # الحصول على آخر رقم تسلسلي
    all_records = sheet.get_all_values()
    next_id = len(all_records) # سيعطي الرقم التالي تلقائياً
    
    # تجهيز الصف
    row = [next_id, name, card_no, total_cost, f"{deductible_percent}%", discount, net_claim, "قيد المعالجة", date_str]
    
    sheet.append_row(row)
    print(f"✅ تم بنجاح إضافة العميل: {name} | الصافي: {net_claim}")

# مثال للاستخدام (يمكنك تغيير هذه القيم لإضافة مريض جديد فوراً)
insert_patient_data("اسم المريض الجديد", "رقم البطاقة", 15000, 20, 1000)
