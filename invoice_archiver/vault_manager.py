import os

# بيانات الخزنة المنظمة (أضف أو عدل المفاتيح هنا دائماً)
vault_content = """
===========================================================
          🔒 خـزنـة الـمـبـرزي الـمركـزيـة (2026) 🔒
===========================================================

1. إعدادات التليجرام (Telegram Bot):
-----------------------------------
- BOT_TOKEN: 7886483584:AAHh7M_T-ZpE8_lEEx6Z_nUo1FmQp9_rF18
- CHAT_ID: 6671043743
- BOT_LINK: https://t.me/MubraziOptics2026Bot

2. الوكلاء الماليون (Financial Agents):
--------------------------------------
- AGENT_NAME: smart_mubrazi_v1.py
- MONITORING: BTC, ETH, SOL, XRP
- LOG_FILE: mubrazi_log.txt

3. مفاتيح التداول (Trading APIs):
---------------------------------
- BINANCE_API_KEY: [سيتم إضافته بعد التوثيق]
- BYBIT_API_KEY: [سيتم إضافته بعد التوثيق]

4. المحفظة والجيت هوب (Wallet & GitHub):
---------------------------------------
- WALLET_TYPE: Trust Wallet (USDT-TRC20)
- GITHUB_USER: [ضع اسم المستخدم هنا]
- EMAIL: Mahboobmabrzy@gmail.com

5. روابط سريعة للإدارة (Admin Links):
------------------------------------
- Google Drive Vault: [ضع رابط مجلدك هنا]
- Binance API Mgt: https://www.binance.com/en/my/settings/api-management

===========================================================
⚠️ تحذير: هذا الملف يحتوي على بيانات سرية، لا تشاركه مع أحد.
===========================================================
"""

def create_vault():
    with open("Mubrazi_Master_Vault.txt", "w") as f:
        f.write(vault_content.strip())
    print("\n✅ تم إنشاء الخزنة المركزية بنجاح!")
    print("📂 اسم الملف: Mubrazi_Master_Vault.txt")
    print("💡 لعرض المفاتيح في أي وقت، اكتب الأمر: cat Mubrazi_Master_Vault.txt\n")

if __name__ == "__main__":
    create_vault()
