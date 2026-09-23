import sys
import os

# إضافة المسار الرئيسي للمشروع تلقائياً
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.models import Base
from sqlalchemy import create_engine

DB_PATH = "mubrazi_database.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def init_database():
    print("جاري إنشاء جداول قاعدة البيانات لنظام المبرزي...")
    Base.metadata.create_all(bind=engine)
    print("تَمَّ إنشاء كافة الجداول بنجاح.")

if __name__ == "__main__":
    init_database()
