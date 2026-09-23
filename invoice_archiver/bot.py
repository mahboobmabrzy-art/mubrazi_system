import telebot
import gspread
import schedule
import time
import threading
import re
import io
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
import pytesseract

# --- الإعدادات ---
API_TOKEN = "8375835755:AAHEFruDL5U7oPBowWM7Evnc5s2eKbf3PIU"
CHANNEL_ID = -1001234567890 
bot = telebot.TeleBot(API_TOKEN)

# --- إعداد جوجل شيت ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("Creds.json", scope)
client = gspread.authorize(creds)

# فتح الصفحات
try:
    spreadsheet = client.open("سجل الفواتير والمصروفات والتسويق")
    sheet_expenses = spreadsheet.worksheet("المصروفات العامة")
except Exception as e:
    print(f"⚠️ خطأ في فتح الملف: {e}")

# --- معالجة الرسائل والصور ---
@bot.message_handler(content_types=['photo', 'text'])
def handle_message(message):
    try:
        text = ""
        if message.content_type == 'photo':
            bot.send_chat_action(message.chat.id, 'typing')
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            image = Image.open(io.BytesIO(downloaded_file))
            text = pytesseract.image_to_string(image, lang="ara+eng")
        else:
            text = message.text

        # تحليل المصروفات
        keywords = ["إيجار", "راتب", "مورد", "مصروف", "فواتير"]
        if any(key in text for key in keywords):
            amounts = re.findall(r'\b\d{3,}\b', text)
            val = amounts[0] if amounts else "0"
            
            # إضافة السطر للشيت
            sheet_expenses.append_row(["مصروف آلي", "", "", val, "نقدي", message.from_user.username])
            bot.reply_to(message, f"✅ تم الأرشفة: مبلغ {val}")
    except Exception as e:
        print(f"Error: {e}")

# --- الجدولة الزمنية ---
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_schedule, daemon=True).start()

print("--- نظام المبرزي المطور قيد التشغيل ---")
bot.polling(none_stop=True)
