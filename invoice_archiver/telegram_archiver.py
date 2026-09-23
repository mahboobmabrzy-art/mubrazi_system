import os
import io
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# 1. إعدادات النظام (المسارات والتوكن المدمج)
BASE_DIR = "/data/data/com.termux/files/home/mubrazi_system"
SA_PATH = os.path.join(BASE_DIR, "service_account.json")
TOKEN = "8375835755:AAGIIpNmF1N_ah4xro4k1NCiSW39GexdR54"

# 2. إعداد الاتصال بـ Google Drive
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SA_PATH, scope)
drive_service = build('drive', 'v3', credentials=creds)

# 3. إعداد التسجيل (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 4. دالة معالجة الصور (الفواتير)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.photo[-1].get_file()
        file_name = f"Invoice_{update.message.date}.jpg"
        
        # تحميل الصورة في الذاكرة
        buf = io.BytesIO()
        await file.download_to_memory(buf)
        buf.seek(0)
        
        # رفع الصورة إلى Google Drive
        file_metadata = {'name': file_name}
        media = {'body': buf, 'mimetype': 'image/jpeg'}
        drive_service.files().create(body=file_metadata, media_body=media).execute()
        
        await update.message.reply_text("✅ تم أرشفة الفاتورة بنجاح في Google Drive!")
        logging.info("تمت أرشفة فاتورة جديدة.")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}")
        logging.error(f"Error: {e}")

# 5. تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🚀 النظام يعمل الآن بنجاح! بانتظار الفواتير...")
    app.run_polling()

if __name__ == "__main__":
    main()
