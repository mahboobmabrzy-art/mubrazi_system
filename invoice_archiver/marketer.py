import os

# المسار الذي يحتوي على ملفاتك البرمجية المنظمة في إمبراطوريتك
BASE_PATH = "/sdcard/My_Empire/01_Programming"

def generate_ad():
    print("\n🔍 جاري فحص ملفاتك لاختيار أفضل منتج للبيع...")
    
    # التأكد من وجود المجلد أولاً
    if not os.path.exists(BASE_PATH):
        print(f"❌ المجلد غير موجود: {BASE_PATH}")
        return

    files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(os.path.join(BASE_PATH, f))]
    
    if not files:
        print("❌ لم يتم العثور على ملفات في مجلد البرمجة. انقل ملفاتك البرمجية إلى مجلد 01_Programming أولاً.")
        return

    selected_file = files[0] # البدء بأول ملف متاح
    file_ext = os.path.splitext(selected_file)[1]

    ad_template = f"""
==================================================
💰 إعلان جاهز لمنتجك الرقمي (انسخه وانشره):
==================================================
Title: Professional {file_ext[1:].upper() if file_ext else 'Tool'} Script for Automation
Description: 
Boost your productivity with this clean, efficient source code. 
Perfect for developers and entrepreneurs looking for ready-to-use solutions.

✅ High Quality Code
✅ Easy to Customize
✅ Instant Download

Price: $5 - $15
==================================================
📂 اسم الملف المختار: {selected_file}
==================================================
"""
    print(ad_template)

if __name__ == "__main__":
    generate_ad()

º
º
º
