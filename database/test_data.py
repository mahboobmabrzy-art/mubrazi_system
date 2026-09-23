import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.models import Customer, Invoice, Payment
from database.init_db import engine
from sqlalchemy.orm import sessionmaker
from modules.medical.services import MedicalService
from modules.accounting.invoice_formatter import InvoiceFormatter

Session = sessionmaker(bind=engine)
session = Session()

def run_test():
    # 1. إضافة عميل تجريبي
    new_customer = Customer(name="عميل تجريبي", phone="770000000", customer_type="regular")
    session.add(new_customer)
    session.commit()

    # 2. إعداد تفاصيل فحص النظر
    optics_info = MedicalService.format_optics_prescription(-1.25, -0.50, 180, -1.50, -0.75, 175, 63.0)

    # 3. إنشاء فاتورة بالترويسة المخصصة
    new_invoice = Invoice(
        customer_id=new_customer.id,
        invoice_number="INV-2026-001",
        item_name="نظارة طبية شاملة العدسات",
        item_type="بصريات",
        total_amount=25000.0,
        paid_amount=10000.0,
        remaining_amount=15000.0,
        details=optics_info
    )
    session.add(new_invoice)
    session.commit()

    # 4. عرض الفاتورة المنسقة
    formatted_text = InvoiceFormatter.format_invoice_text(
        invoice_number=new_invoice.invoice_number,
        customer_name=new_customer.name,
        customer_phone=new_customer.phone,
        item_name=new_invoice.item_name,
        item_type=new_invoice.item_type,
        details_table=[{"desc": "إطار نظارة + عدسات مضادة للإنعكاس", "price": 25000.0}],
        total_amount=new_invoice.total_amount,
        paid_amount=new_invoice.paid_amount
    )

    print(formatted_text)
    print("\nتَمَّت أتمتة واختبار البيانات بنجاح.")

if __name__ == "__main__":
    run_test()
