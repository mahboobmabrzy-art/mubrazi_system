import datetime
from mubariz_bot import append_to_sheet

def archive_normal_customer(name, phone, price, description):
    """أرشفة بيانات العملاء العاديين لمركز المبرزي"""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [date_str, "عميل عادي", name, phone, f"{price} USDT", description]
    return append_to_sheet("Mubarizi_Financial_System", row)

def archive_insurance_claim(company_name, patient_name, card_number, prescription_details):
    """أرشفة مطالبات التأمين الصحي الطبي"""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [date_str, f"تأمين: {company_name}", patient_name, f"رقم بطاقة: {card_number}", "-", prescription_details]
    return append_to_sheet("Mubarizi_Financial_System", row)

def archive_bank_deposit(bank_name, account_number, amount, depositor_name):
    """أرشفة الحوالات والإيداعات البنكية"""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [date_str, f"إيداع بنكي: {bank_name}", depositor_name, f"حساب: {account_number}", f"{amount} USDT", "إيداع مالي"]
    return append_to_sheet("Mubarizi_Financial_System", row)

if __name__ == "__main__":
    print("🚀 جاري اختبار ترحيل القوالب الثلاثة لنظام المبرزي...")
    archive_normal_customer("محمد المبرزي", "770375650", "150", "نظارة طبية متكاملة")
    archive_insurance_claim("شركة كير", "أحمد علي", "INS-9982", "فحص نظر وعدسات سماعات")
    archive_bank_deposit("بنك التضامن", "10203040", "500", "محبوب مبارزي")
