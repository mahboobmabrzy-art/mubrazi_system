import os
import re
import tempfile

import telebot

from google.cloud import vision
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# =========================
# Config (غيّر القيم هنا)
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "
8375835755:AAEo0XJlwETemRfD0smzp53IXo-oL9hvrRg")
SERVICE_ACCOUNT_FILE = "mubrazi-financial-secrets.json"

# Drive + Sheets scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]

# IDs
DRIVE_FOLDER_ID = "YOUR_GOOGLE_DRIVE_FOLDER_ID"
SPREADSHEET_ID = "YOUR_GOOGLE_SHEETS_ID"
SHEET_RANGE = "الأرشيف العام!A:D"  # تأكد أنها موجودة بالاسم العربي

# الحالة
DEFAULT_STATUS = "معلق التدقيق"


# =========================
# Services
# =========================
BOT = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)

CREDS = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
DRIVE_SERVICE = build("drive", "v3", credentials=CREDS)
SHEETS_SERVICE = build("sheets", "v4", credentials=CREDS)


# =========================
# OCR helpers
# =========================
def clean_ocr_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_image(image_path: str) -> str:
    client = vision.ImageAnnotatorClient(credentials=CREDS)
    with open(image_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if response.error and response.error.message:
        raise RuntimeError(response.error.message)

    texts = response.text_annotations
    return texts[0].description if texts else ""


def upload_to_drive(local_path: str, filename: str) -> str:
    file_metadata = {"name": filename, "parents": [DRIVE_FOLDER_ID]}
    media = MediaFileUpload(local_path, mimetype="image/jpeg")

    uploaded = DRIVE_SERVICE.files().create(
        body=file_metadata,
        media_body=media,
        fields="webViewLink"
    ).execute()

    return uploaded.get("webViewLink", "")


# =========================
# Telegram Handler
# =========================
@BOT.message_handler(content_types=["photo"])
def handle_invoice_image(message):
    chat_id = message.chat.id
    processing_msg = BOT.reply_to(message, "⚙️ جاري رفع الفاتورة + OCR + الحفظ في Google Sheets...")

    local_path = None
    try:
        # أفضل صورة = آخر عنصر غالبًا
        file_id = message.photo[-1].file_id
        file_info = BOT.get_file(file_id)
        downloaded_bytes = BOT.download_file(file_info.file_path)

        # ملف مؤقت آمن
        fd, local_path = tempfile.mkstemp(prefix=f"invoice_{message.message_id}_", suffix=".jpg")
        os.close(fd)
        with open(local_path, "wb") as f:
            f.write(downloaded_bytes)

        filename = os.path.basename(local_path)

        # 1) رفع Drive
        drive_link = upload_to_drive(local_path, filename)

        # 2) OCR
        ocr_text = extract_text_from_image(local_path)
        ocr_text_clean = clean_ocr_text(ocr_text)

        # 3) سجل في Sheets
        # الأعمدة: A=NOW(), B=Drive link, C=ملخص/نص، D=الحالة
        summary = (ocr_text_clean[:1000] if ocr_text_clean else "")
        row_data = [
            "=NOW()",
            drive_link,
            summary,
            DEFAULT_STATUS
        ]

        SHEETS_SERVICE.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_RANGE,
            valueInputOption="USER_ENTERED",
            body={"values": [row_data]}
        ).execute()

        BOT.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text="✅ تم! تم رفع الصورة إلى Google Drive، واستخراج OCR، وتسجيلها في Google Sheets."
        )

    except Exception as e:
        BOT.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=f"❌ خطأ أثناء المعالجة: {e}"
        )
    finally:
        # حذف الملف المؤقت
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
            except:
                pass


if __name__ == "__main__":
    print("Invoice Archiver (single) يعمل الآن...")
    BOT.infinity_polling(skip_pending=True)
،
