from mubariz_bot import append_to_sheet
import datetime

# تجهيز سطر بيانات تجريبي لمركز المبرزي [التاريخ والوقت، نوع العملية، المبلغ، البيان]
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
test_data = [current_time, "فحص نظام", "100 USDT", "عملية تجريبية لربط جداول جوجل بنجاح"]

# اسم جدول البيانات الخاص بك في حساب Google Drive (يرجى التأكد من مطابقة الاسم لاحقاً)
SHEET_NAME = "Mubarizi_Financial_System"

print(f"🔄 جاري محاولة إرسال البيانات إلى جدول '{SHEET_NAME}'...")
append_to_sheet(SHEET_NAME, test_data)
