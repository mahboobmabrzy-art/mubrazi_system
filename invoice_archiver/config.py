import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./al_mubarazi.db")
    ADMIN_CHAT_ID = 5118430414
    
    # مسارات التخزين
    INVOICE_PHOTOS_DIR = "storage/invoices"
    
    @staticmethod
    def init_app():
        # التأكد من وجود مجلدات التخزين
        os.makedirs(Config.INVOICE_PHOTOS_DIR, exist_ok=True)

if __name__ == "__main__":
    # اختبار التحميل
    print(f"Token: {Config.TELEGRAM_BOT_TOKEN}")
