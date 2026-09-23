from PIL import Image
import io
from googleapiclient.http import MediaIoBaseUpload

def safe_upload(file_path, drive_service, folder_id):
    # 1. ضغط الصورة فوراً لتناسب سرعة الإنترنت
    img = Image.open(file_path)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=35, optimize=True) # جودة 35 مثالية جداً
    buffer.seek(0)
    
    # 2. تفعيل الرفع المستأنف (حل الخطأ 103)
    media = MediaIoBaseUpload(buffer, mimetype='image/jpeg', resumable=True)
    request = drive_service.files().create(
        body={'name': 'invoice_mubariz.jpg', 'parents': [folder_id]},
        media_body=media, fields='id'
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"📡 تقدم الرفع: {int(status.progress() * 100)}%")
    return response.get('id')

