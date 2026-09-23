import os, time, json, requests

DATA_FILE = "offline_data.json"

def check_internet():
    try:
        requests.get("https://8.8.8.8", timeout=3)
        return True
    except:
        return False

def run_task():
    # منطق جلب الأسعار وحفظها محلياً
    data = {"timestamp": time.time(), "status": "pending"}
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    
    if check_internet():
        print("الإنترنت متوفر.. جاري مزامنة البيانات وتحديث Google Sheets...")
        # هنا يتم استدعاء كود الرفع الخاص بك
        os.remove(DATA_FILE)
    else:
        print("لا يوجد إنترنت.. تم حفظ البيانات محلياً للرفع لاحقاً.")

if __name__ == "__main__":
    run_task()
