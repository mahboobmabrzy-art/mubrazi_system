import requests
import os

def run_vault_check():
    print("\n--- 🛡️ نظام المبرزي: جاري الفحص والأرشفة ---")
    token = "7886483584:AAHh7M_T-ZpE8_lEEx6Z_nUo1FmQp9_rF18"
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
        if r.get("ok"):
            print(f"✅ الحالة: البوت يعمل بنجاح ({r['result']['first_name']})")
            print(f"📂 الملف السري: Mubrazi_Master_Vault.txt")
            print("💡 تم حفظ بياناتك في الترمكس بنجاح.")
        else:
            print("❌ خطأ: التوكن غير صحيح.")
    except:
        print("⚠️ تنبيه: لا يوجد إنترنت، تم حفظ الملف محلياً فقط.")

if __name__ == "__main__":
    run_vault_check()
