import logging
from invoice_archiver import telegram_archiver

# إعداد السجل لتتبع أي أخطاء
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MubarizSystem:
    def start_archiving(self):
        try:
            logger.info("جاري بدء تشغيل وحدة الأرشفة...")
            telegram_archiver.main() # استدعاء الدالة main من الملف المستورد
        except Exception as e:
            logger.error(f"حدث خطأ أثناء التشغيل: {e}")

if __name__ == "__main__":
    system = MubarizSystem()
    system.start_archiving()
