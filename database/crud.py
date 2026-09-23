from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, Customer, MedicalRecord, Invoice, MarketingCampaign

DATABASE_URL = "sqlite:///./al_mubarazi.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Customer Operations
def create_customer(db, name, phone):
    customer = Customer(name=name, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customer_by_phone(db, phone):
    return db.query(Customer).filter(Customer.phone == phone).first()

# Medical Record Operations
def add_medical_record(db, customer_id, record_type, **kwargs):
    record = MedicalRecord(customer_id=customer_id, record_type=record_type, **kwargs)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# Invoice Operations
def create_invoice(db, customer_id, invoice_number, total_amount, profit, item_type, photo_path=None):
    invoice = Invoice(
        customer_id=customer_id,
        invoice_number=invoice_number,
        total_amount=total_amount,
        profit=profit,
        item_type=item_type,
        invoice_photo_path=photo_path
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def get_total_sales(db):
    from sqlalchemy import func
    return db.query(func.sum(Invoice.total_amount)).scalar() or 0.0

def get_total_profit(db):
    from sqlalchemy import func
    return db.query(func.sum(Invoice.profit)).scalar() or 0.0
