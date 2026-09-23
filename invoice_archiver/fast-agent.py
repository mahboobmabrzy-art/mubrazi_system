import requests
import time
import hmac
import hashlib

def get_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    res = requests.get(url).json()
    return float(res['price'])

def get_bybit_price(symbol="BTCUSDT"):
    url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
    res = requests.get(url).json()
    return float(res['result']['list'][0]['lastPrice'])

print("--- تم إطلاق الوكيل السريع لإنهاء المهام ---")

while True:
    try:
        p1 = get_binance_price()
        p2 = get_bybit_price()
        gap = abs(p1 - p2)
        gap_pct = (gap / min(p1, p2)) * 100
        
        print(f"Binance: {p1} | Bybit: {p2}")
        print(f"فجوة السعر: {gap_pct:.4f}%")
        
        if gap_pct > 0.1:
            print("🚀 المهمة 2: تم رصد فجوة بنجاح!")
            
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
    
    time.sleep(5)
