import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import gspread
from datetime import datetime

# الإعدادات من ملف env الخاص بك
TOKEN = '8375835755:AAEfwFE_V0HPwVyEcLRyi_J77NVphsaCedE'
DRIVE_FOLDER_ID = '1CFTl8veKkvXf-LqsL-F-GUyzOH8-zUax'
SHEET_ID = '1mkVedQYB5Qt28YlaZ4uQ18NipMDZSdLYSLnNO3YJy74'

# إعداد صلاحيات جوجل (تأكد من وجود ملف credentials.json في نفس المجلد)
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_ID).sheet1

async def handle_invoice_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. استلام الصورة
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    await photo_file.download_to_drive(file_path)
    
    await update.message.reply_text("جاري معالجة الفاتورة ورفعها للأرشيف...")

    # 2. رفع الصورة إلى Google Drive
    file_metadata = {'name': file_path, 'parents': [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    file_link = uploaded_file.get('webViewLink')

    # 3. إضافة البيانات إلى Google Sheet
    # الترتيب: الرقم التسلسلي، التاريخ، اسم العميل، الصنف، الماركة، اللون، الإجمالي، المدفوع، المتبقي، ملاحظات (رابط الصورة)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_row = ["آلي", now, "عميل جديد", "نظارة", "-", "-", "0", "0", "0", f"رابط الصورة: {file_link}"]
    sheet.append_row(new_row)

    await update.message.reply_text(f"✅ تم الأرشفة بنجاح!\nرابط المستند: {file_link}")
    os.remove(file_path) # حذف الصورة المؤقتة من الهاتف

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_invoice_photo))
    print("Bot is running...")
    app.run_polling()
