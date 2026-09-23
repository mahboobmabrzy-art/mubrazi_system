import telebot
import gspread
import schedule
import time
import threading
import re
import io
import os
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from datetime import datetime
import logging

# ⚙️ إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔐 تحميل المتغيرات
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(API_TOKEN)

# 📊 الربط مع Google Sheets
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet_expenses = client.open("سجل الفواتير والمصروفات والتسويق").worksheet("المصروفات العامة")
    logger.info("✅ تم الاتصال بـ Google Sheets بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في الاتصال: {e}")

# 📨 معالج الرسائل
@bot.message_handler(content_types=['photo', 'text'])
def handle_message(message):
    try:
        text = message.text if message.content_type == 'text' else "صورة مستلمة"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # استخراج المبلغ (بحث بسيط عن الأرقام)
        amount_match = re.search(r"(\d+)", text)
        amount = amount_match.group(1) if amount_match else "0"

        # تسجيل في الجدول
        sheet_expenses.append_row(["مصروف عام", timestamp, amount, "نقدي", message.from_user.username or "مجهول", "✅"])
        
        bot.reply_to(message, f"✅ تم التسجيل بنجاح في سجل المبرزي!\n💰 المبلغ: {amount} ريال")
        bot.send_message(CHANNEL_ID, f"📢 إشعار جديد:\nنوع: مصروف\nمبلغ: {amount}\nتوقيت: {timestamp}")
        
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")

if __name__ == "__main__":
    print("🚀 نظام المبرزي للبصريات يعمل الآن...")
    bot.polling()
