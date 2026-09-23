import telebot
import gspread
import re
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import datetime
import logging

# ⚙️ إعداد السجلات (Logs) لتتبع العمليات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔐 تحميل المتغيرات من ملف .env
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telebot.TeleBot(API_TOKEN)

# 📊 تعريف متغير ورقة العمل كمتغير عام لضمان الوصول إليه في كل الدوال
sheet_expenses = None

def connect_sheets():
    """دالة للاتصال بـ Google Sheets وإعداد المتغيرات"""
    global sheet_expenses
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # تأكد من وجود ملف credentials.json في نفس المجلد داخل Termux
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        
        # فتح ملف السجل والورقة المحددة (تأكد من تطابق الأسماء تماماً)
        spreadsheet = client.open("سجل الفواتير والمصروفات والتسويق")
        sheet_expenses = spreadsheet.worksheet("المصروفات العامة")
        
        logger.info("✅ تم الاتصال بـ Google Sheets بنجاح")
    except Exception as e:
        logger.error(f"❌ فشل الاتصال بالجداول: {e}")

# محاولة الاتصال الأولية عند تشغيل الملف
connect_sheets()

@bot.message_handler(content_types=['photo', 'text'])
def handle_message(message):
    global sheet_expenses
    try:
        # صمام أمان: إذا فقد الاتصال، حاول إعادة الاتصال قبل المعالجة
        if sheet_expenses is None:
            connect_sheets()
            if sheet_expenses is None:
                bot.reply_to(message, "❌ النظام غير متصل بقاعدة البيانات حالياً.")
                return

        # تحديد النص سواء كان رسالة نصية أو شرحاً لصورة (Caption)
        text = message.text if message.content_type == 'text' else message.caption
        if not text:
            text = "محتوى بدون نص"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # استخراج أول رقم يظهر في النص ليكون هو "المبلغ"
        amount_match = re.search(r"(\d+)", text)
        amount = amount_match.group(1) if amount_match else "0"

        # إضافة البيانات إلى Google Sheets في سطر جديد
        sheet_expenses.append_row([
            "مصروف عام", 
            timestamp, 
            amount, 
            "نقدي", 
            message.from_user.username or "مجهول",             "✅"
        ])

        # الرد على المستخدم وإرسال إشعار للقناة المحددة
        bot.reply_to(message, f"✅ تم التسجيل بنجاح في سجل المبرزي!\n💰 المبلغ: {amount} ريال")
        bot.send_message(CHANNEL_ID, f"📢 إشعار جديد:\n• النوع: مصروف\n• المبلغ: {amount}\n• التوقيت: {timestamp}")

    except Exception as e:
        logger.error(f"❌ خطأ معالجة: {e}")
        bot.reply_to(message, "⚠️ حدث خطأ تقني أثناء محاولة الحفظ.")

if __name__ == "__main__":
    print("🚀 نظام المبرزي للبصريات (AL-MUBRAZI) يعمل الآن...")
    # none_stop=True تضمن عدم توقف البوت عند حدوث أخطاء بسيطة في الاتصال
    bot.polling(none_stop=True
