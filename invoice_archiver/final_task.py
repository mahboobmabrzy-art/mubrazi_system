import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. إعداد الاتصال
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# 2. فتح ملف جوجل شيت
# ملاحظة: تأكد من مشاركة ملف الشيت مع البريد الموجود داخل credentials.json
try:
    sheet = client.open("كشف نفقات مؤمني كاك للتأمين الصحي").sheet1
except Exception as e:
    print(f"❌ لم يتم العثور على الملف. تأكد من الاسم في جوجل شيت. {e}")
    exit()

def setup_professional_columns():
    # تنظيف الجدول بالكامل وإعداد المسميات المطلوبة
    sheet.clear()
    headers = [
        "م", 
        "اسم المريض", 
        "رقم بطاقة التأمين", 
        "إجمالي الكلفة", 
        "نسبة التحمل", 
        "الخصم الإضافي", 
        "صافي المطالبة", 
        "رقم الكود", 
        "التاريخ والوقت"
    ]
    sheet.insert_row(headers, 1)
    print("✅ تم إعداد الأعمدة الاحترافية وتنظيف الجدول بنجاح.")

def add_entry(m, name, card_no, cost, deductible, discount, code):
    # الحساب التلقائي لصافي المطالبة لضمان الدقة المحاسبية
    net_claim = cost - (deductible + discount)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    row = [m, name, card_no, cost, deductible, discount, net_claim, code, now]
    sheet.append_row(row)
    print(f"✅ تمت إضافة بيانات العميل: {name}")

# تنفيذ المهام
setup_professional_columns()

# إضافة صف بيانات حقيقي (بناءً على الكشف الذي أرفقته سابقاً)
add_entry(1, "افكار مرشد احمد الذماري", "239*189504", 20000, 4000, 6000, "1478491")
