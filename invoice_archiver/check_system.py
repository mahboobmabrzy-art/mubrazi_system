import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name('vault/service_account.json', scope)
    client = gspread.authorize(creds)
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1MH-Q6xIYRmctyN9v3gINP4a7HkS_lGoKzqWB_y5rUsk/edit"
    spreadsheet = client.open_by_url(sheet_url)
    sheet = spreadsheet.get_worksheet(0)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    row = [now, "اختبار_نظام_المبرزي", "100", "0", "0", "100"]
    
    sheet.append_row(row)
    print("\n✅ نجح الربط! تم إضافة سطر اختبار لجدول نفقات كاك بنجاح.")

except Exception as e:
    print(f"\n❌ خطأ: {e}")
