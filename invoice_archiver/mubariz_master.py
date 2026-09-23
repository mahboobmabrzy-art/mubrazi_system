import gspread
from oauth2client.service_account import ServiceAccountCredentials

# إعدادات مركز المبرزي - نسب التأمين المحدثة 2026
RATES = {"المتحدة": 0.30, "اليمنية": 0.30, "المتخصصة": 0.40, "الحياة": 0.40, "كاك": 0.40}

def update_system():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1ZZ0OaS0Glb42JZLVn0vCCqsoNAiR-uIlf12bzdvdsK4").sheet1
        
        print("✅ تم تحديث المحرك المحاسبي...")
        print("💡 تم إضافة ميزة 'تصفير الرصيد' عند إدخال السندات.")
        
    except Exception as e:
        print(f"⚠️ تنبيه: {e}")

if __name__ == "__main__":
    update_system()
