import requests
import base64
import json

# سنقوم بوضع الـ API KEY الخاص بك هنا لاحقاً
API_KEY = "YOUR_API_KEY_HERE"
url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"

def analyze_product(image_path):
    with open(image_path, "rb") as image:
        img_base64 = base64.b64encode(image.read()).decode()

    payload = {
        "requests": [{
            "image": {"content": img_base64},
            "features": [{"type": "LABEL_DETECTION", "maxResults": 5}]
        }]
    }

    response = requests.post(url, json=payload)
    return response.json()

# مثال للاستخدام
# result = analyze_product("test.jpg")
# print(json.dumps(result, indent=2))
