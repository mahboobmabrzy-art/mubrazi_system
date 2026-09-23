# نظام المبرزي للبصريات والسمعيات المتكامل

## نظرة عامة
يهدف هذا المشروع إلى دمج كافة الأنظمة البرمجية لـ "المبرزي للبصريات والسمعيات" في نظام واحد متكامل ونظيف. سيشمل النظام الوظائف المحاسبية والمالية، والنظام الطبي والتقني، ونظام الأتمتة التسويقية، مع واجهة تحكم عبر Telegram Bot، وتشغيل في بيئة Termux على أجهزة Android.

## الهيكل المعماري
سيعتمد النظام على بنية معمارية معيارية (Modular Architecture) باستخدام لغة Python، حيث سيتم تقسيم الوظائف الرئيسية إلى وحدات مستقلة (Modules) لضمان سهولة الصيانة والتوسع.

- **المحرك الرئيسي (main.py)**: نقطة الدخول الرئيسية للتطبيق، يدير التفاعلات بين الوحدات المختلفة وواجهة Telegram Bot. يتعامل مع الأوامر الأساسية والرسائل الواردة من المستخدمين.
- **وحدة النظام المحاسبي والمالي (`modules/accounting`)**: تتولى إدارة المبيعات، الأرباح، وتتبع مبيعات النظارات والسماعات. توفر وظائف لتسجيل المبيعات، حساب الأرباح، وإنشاء تقارير مالية موجزة.
- **وحدة النظام الطبي والتقني (`modules/medical`)**: تتعامل مع بيانات فحص النظر، مقاسات السمع، وسجل العملاء. تسمح بحفظ بيانات الفحوصات الطبية واسترجاع السجل الكامل للعميل.
- **وحدة الأتمتة التسويقية (`modules/marketing`)**: مسؤولة عن الربط مع Telegram ونشر العروض الترويجية. توفر وظائف لإرسال رسائل جماعية للعملاء وتوليد نصوص العروض التسويقية.
- **وحدة قاعدة البيانات (`database`)**: تدير التفاعلات مع قاعدة بيانات SQLite الموحدة. تحتوي على تعريفات النماذج (Models) وعمليات الإنشاء، القراءة، التحديث، الحذف (CRUD).
- **وحدة الإعدادات والأمان (`config.py`)**: تتعامل مع تحميل المتغيرات البيئية (Environment Variables) من ملف `.env` وتوفير إعدادات التطبيق. تضمن عزل المفاتيح الحساسة والروابط.
- **وحدة الأدوات المساعدة (`utils`)**: تحتوي على وظائف مساعدة عامة يمكن استخدامها عبر الوحدات المختلفة.

## هيكل المشروع (Project Structure)
```
./
├── main.py                     # المحرك الرئيسي للتطبيق وواجهة Telegram Bot
├── config.py                   # ملف لإدارة الإعدادات وتحميل المتغيرات البيئية
├── .env.example                # مثال لملف المتغيرات البيئية (يجب نسخه وتعديله إلى .env)
├── database/
│   ├── __init__.py
│   ├── models.py               # تعريف نماذج قاعدة البيانات (SQLAlchemy)
│   └── crud.py                 # عمليات الإنشاء، القراءة، التحديث، الحذف (CRUD)
├── modules/
│   ├── __init__.py
│   ├── accounting/
│   │   ├── __init__.py
│   │   └── services.py         # منطق الأعمال والخدمات للمحاسبة
│   ├── medical/
│   │   ├── __init__.py
│   │   └── services.py         # منطق الأعمال والخدمات للجانب الطبي
│   └── marketing/
│       ├── __init__.py
│       └── services.py         # منطق الأعمال والخدمات للتسويق (بما في ذلك Telegram Bot handlers)
├── utils/
│   ├── __init__.py
│   └── helpers.py              # وظائف مساعدة عامة (يمكن إضافة المزيد حسب الحاجة)
├── requirements.txt            # قائمة بالمكتبات المطلوبة (لتثبيتها باستخدام pip)
├── install.sh                  # سكريبت التثبيت والإعداد لبيئة Termux
└── README.md                   # وصف المشروع والهيكل والتعليمات
```

## التقنيات المستخدمة
- **اللغة**: Python 3.x
- **قاعدة البيانات**: SQLite (للتخزين المحلي)، مع إمكانية التوسع لاحقاً باستخدام Google Sheets API إذا لزم الأمر.
- **إدارة المتغيرات البيئية**: `python-dotenv` [1]
- **Telegram Bot**: `python-telegram-bot` [2]
- **ORM (Object-Relational Mapping)**: SQLAlchemy (للتفاعل مع قاعدة البيانات) [3]

## بيئة التشغيل: Termux على أجهزة Android
تم تصميم هذا النظام ليعمل بكفاءة في بيئة Termux على أجهزة Android. Termux هو محاكي طرفية قوي يوفر بيئة Linux كاملة على جهازك المحمول، مما يتيح تشغيل تطبيقات Python وإدارة قواعد البيانات المحلية.

### خطوات التثبيت والإعداد في Termux
1.  **تثبيت Termux**: قم بتنزيل وتثبيت تطبيق Termux من [F-Droid](https://f-droid.org/packages/com.termux/) أو [متجر Google Play](https://play.google.com/store/apps/details?id=com.termux).
2.  **تشغيل سكريبت التثبيت**: بعد فتح Termux، قم بتنزيل سكريبت `install.sh` وتشغيله:
    ```bash
    pkg update && pkg upgrade
    pkg install git -y
    git clone https://github.com/your_username/al_mubarazi_system.git # استبدل بالرابط الصحيح للمستودع
    cd al_mubarazi_system
    chmod +x install.sh
    ./install.sh
    ```
3.  **تعديل ملف `.env`**: سيقوم السكريبت بإنشاء ملف `.env` بناءً على `.env.example`. يجب عليك تعديل هذا الملف وإضافة `TELEGRAM_BOT_TOKEN` الخاص بالبوت و `ADMIN_CHAT_ID` الخاص بك.
    -   **للحصول على `TELEGRAM_BOT_TOKEN`**: تحدث مع BotFather على Telegram ([@BotFather](https://t.me/BotFather)) لإنشاء بوت جديد والحصول على التوكن.
    -   **للحصول على `ADMIN_CHAT_ID`**: أرسل رسالة إلى البوت الخاص بك، ثم قم بزيارة `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` في متصفح الويب الخاص بك للعثور على `chat_id` الخاص بك.
4.  **تشغيل البوت**: بعد تعديل ملف `.env`، يمكنك تشغيل البوت باستخدام الأمر:
    ```bash
    python main.py
    ```

## الاستخدام عبر Telegram Bot
بعد تشغيل البوت، يمكنك التفاعل معه عبر Telegram:
-   ابدأ المحادثة مع البوت باستخدام الأمر `/start`.
-   ستظهر لك لوحة مفاتيح تحتوي على الأقسام الرئيسية للنظام (المحاسبة، الجانب الطبي، التسويق، سجل العملاء).
-   اختر القسم المطلوب للوصول إلى وظائفه.
-   للبحث عن عميل، يمكنك إرسال رقم هاتفه مباشرة إلى البوت.

## الخطوات التالية (قيد التطوير)
-   توسيع وظائف قسم المحاسبة لتشمل تتبع المخزون وإدارة المصروفات.
-   تطوير واجهة إدخال بيانات فحص النظر والسمع بشكل تفاعلي عبر البوت.
-   إضافة وظيفة التقاط صور الفواتير وأرشفتها.
-   تحسين موديول التسويق ليشمل استهداف العملاء بناءً على سجلهم الطبي أو الشرائي.
-   تكامل مع Google Sheets API لتخزين البيانات بشكل اختياري.

## المراجع
[1] python-dotenv: A Python module that allows you to load environment variables from a .env file. Available at: [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
[2] python-telegram-bot: A library that simplifies the interaction with the Telegram Bot API. Available at: [https://python-telegram-bot.org/](https://python-telegram-bot.org/)
[3] SQLAlchemy: The Python SQL Toolkit and Object Relational Mapper. Available at: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
