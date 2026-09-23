import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# إعداد الاتصال
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# حاول فتح الملف
try:
    # ملاحظة: الاسم يجب أن يطابق اسم الملف في جوجل شيت حرفياً
    sheet = client.open("كشف نفقات مؤمني كاك للتأمين الصحي").sheet1
except Exception as e:
    print(f"❌ لم يتم العثور على الملف. تأكد من الاسم. الخطأ: {e}")
    exit()

def setup_mubariz_sheet():
    # تنظيف الجدول وإعداد الأعمدة المطلوبة
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
        "التاريخ"
    ]
    sheet.insert_row(headers, 1)
    print("✅ تم إعداد الأعمدة المطلوبة بنجاح.")

def add_entry(m, name, card_no, cost, deductible, discount, code):
    # الحساب التلقائي لصافي المطالبة لضمان الدقة المالية
    net_claim = cost - (deductible + discount)
    date_now = datetime.now().strftime("%Y-%m-%d")
    
    row = [m, name, card_no, cost, deductible, discount, net_claim, code, date_now]
    sheet.append_row(row)
    print(f"✅ تمت أرشفة بيانات العميل: {name}")

# تنفيذ المهمة
setup_mubariz_sheet()
# إضافة بيانات العميل (كمثال للتأكد من نجاح العمل)
add_entry(1, "افكار مرشد احمد الذماري", "239*189504", 20000, 4000, 6000, "1478491")

