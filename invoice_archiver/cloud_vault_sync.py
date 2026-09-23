import os
import json

# --- إعدادات الخزنة ---
VAULT_FILE = "Mubrazi_Master_Vault.txt"

def update_vault():
    print("\n--- 📝 تحديث الخزنة المركزية ---")
    print("يرجى لصق البيانات المشتتة هنا (اضغط Ctrl+D عند الانتهاء):")
    
    # استقبال البيانات المنسوخة من الواتس/الملاحظات
    data = []
    try:
        while True:
            line = input()
            data.append(line)
    except EOFError:
        pass
    
    final_content = "\n".join(data)
    
    # 1. الحفظ محلياً في الترمكس
    with open(VAULT_FILE, "a") as f:
        f.write(f"\n--- تحديث جديد بتاريخ {os.popen('date').read()} ---\n")
        f.write(final_content)
    
    print(f"\n✅ تم الحفظ محلياً في {VAULT_FILE}")
    
    # 2. التجهيز للرفع إلى Google Drive (عبر ملف JSON المعتمد سابقاً)
    print("🔄 جاري مزامنة البيانات مع Google Drive...")
    # ملاحظة: سنستخدم هنا مكتبة pydrive أو google-api-python-client التي سنقوم بتثبيتها غداً
    print("⚠️ ملاحظة: الربط السحابي يتطلب تفعيل Service Account الذي أنشأناه.")

if __name__ == "__main__":
    update_vault()
