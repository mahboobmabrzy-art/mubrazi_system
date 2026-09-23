import os
import requests
import re
from cryptography.fernet import Fernet
from datetime import datetime

# إعدادات النظام الموحدة
BOT_TOKEN = "7339129524:AAEOvU974vCUnRPlE_0D0K4XvV0VvK6mC6c"
CHAT_ID = "1135899912"
BASE_DIR = os.path.expanduser("~/Mubrazi_Master")

PATHS = {
    "1": os.path.join(BASE_DIR, "Finance_Vault/transactions.txt"),
    "2": os.path.join(BASE_DIR, "Marketing_Agent/ads_vault.txt"),
    "3": os.path.join(BASE_DIR, "Engineering_Agent/links_archive.txt"),
    "key": os.path.join(BASE_DIR, ".vault_key.key")
}

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except: pass

def smart_process(text):
    """المعالج الآلي للنصوص"""
    # فحص إذا كان النص كود برمجياً (يحتوي على علامات برمجية)
    if any(tag in text for tag in ["def ", "import ", "class ", "function(", "const "]):
        category = "3" # Engineering/Code
        notif = "🛠️ معالجة كود برمجي جديد"
    # فحص إذا كان نصاً تسويقياً (يحتوي على رموز ترويجية)
    elif any(tag in text for tag in ["خصم", "عرض", "سعر", "%", "USDT", "اربح"]):
        category = "2" # Marketing
        notif = "📢 معالجة نص تسويقي فيروسي"
    else:
        category = "1" # General/Finance
        notif = "📝 معالجة بيانات عامة"
    return category, notif

def main():
    if not os.path.exists(PATHS["key"]):
        key = Fernet.generate_key()
        with open(PATHS["key"], "wb") as kf: kf.write(key)
    f = Fernet(open(PATHS["key"], "rb").read())
    
    while True:
        os.system('clear')
        print("=== AL-MUBRAZI SMART AGENT V2 ===")
        print("قم بلصق النص (تسويق، كود، أو مالية) هنا مباشرة:")
        print("أو اكتب 'exit' للخروج.")
        
        user_input = input("\n[Paste Here]: ")
        
        if user_input.lower() == 'exit': break
        
        # المعالجة الآلية دون تدخل المستخدم
        cat, msg_header = smart_process(user_input)
        entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {user_input}"
        
        with open(PATHS[cat], "a") as file:
            file.write(f.encrypt(entry.encode()).decode() + "\n")
        
        send_telegram(f"{msg_header}\n\nالمحتوى:\n{user_input}")
        print(f"\n✅ {msg_header} وتم الحفظ والتشفير."); input("اضغط Enter للمتابعة...")

if __name__ == "__main__":
    main()
