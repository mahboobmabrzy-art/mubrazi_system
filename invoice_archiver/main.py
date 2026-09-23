import requests
import time

def check_usdt_balance(address):
    try:
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        r = requests.get(url).json()
        if 'data' in r and len(r['data']) > 0 and 'trc20' in r['data'][0]:
            for token in r['data'][0]['trc20']:
                if 'TR7NHqjekQXgtCi8q8ZY4pL8otSzgjLj6t' in token:
                    amount = int(token['TR7NHqjekQXgtCi8q8ZY4pL8otSzgjLj6t'])
                    return amount / 1000000
        return 0.0
    except Exception as e:
        print(f"Error: {e}")
        return 0.0

print("تم إصلاح الكود بنجاح.")
