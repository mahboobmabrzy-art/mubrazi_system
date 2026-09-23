from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    medical_records = relationship("MedicalRecord", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    record_type = Column(String(20))  # 'optics' or 'audiology'
    
    # Optics data
    right_eye_sphere = Column(String(10))
    right_eye_cylinder = Column(String(10))
    right_eye_axis = Column(String(10))
    left_eye_sphere = Column(String(10))
    left_eye_cylinder = Column(String(10))
    left_eye_axis = Column(String(10))
    
    # Audiology data
    hearing_loss_level = Column(String(50))
    audiogram_notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    customer = relationship("Customer", back_populates="medical_records")

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    invoice_number = Column(String(50), unique=True)
    total_amount = Column(Float)
    profit = Column(Float)
    item_type = Column(String(20))  # 'glasses' or 'hearing_aid'
    invoice_photo_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="invoices")

class MarketingCampaign(Base):
    __tablename__ = 'marketing_campaigns'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    target_audience = Column(String(50))  # 'all', 'optics', 'audiology'
    sent_at = Column(DateTime, default=datetime.utcnow)
