from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    customer_type = Column(String(20), default='regular')  # 'regular' أو 'insurance'
    created_at = Column(DateTime, default=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")

class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    invoice_number = Column(String(50), unique=True, nullable=False)
    
    # حقول الترويسة العلوية (فوق الجدول)
    item_name = Column(String(100))  # اسم الصنف
    item_type = Column(String(50))   # نوع الصنف (بصريات / سمعيات)
    
    total_amount = Column(Float, nullable=False, default=0.0)
    paid_amount = Column(Float, default=0.0)
    remaining_amount = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    details = Column(Text)  # تفاصيل الجدول والمقاسات
    invoice_photo_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    receipt_number = Column(String(50), unique=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(20), default='cash')
    created_at = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="payments")
    customer = relationship("Customer", back_populates="payments")

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketingCampaign(Base):
    __tablename__ = 'marketing_campaigns'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    target_audience = Column(String(50))
    sent_at = Column(DateTime, default=datetime.utcnow)

class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    record_type = Column(String(50))
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
