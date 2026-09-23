#!/bin/bash

echo "بدء إعداد بيئة Termux لنظام المبرزي المتكامل..."

# 1. تحديث وتثبيت الحزم الأساسية
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install git -y
pkg install openssl-tool -y
pkg install libcrypt -y

# 2. تثبيت pip
python -m ensurepip --default-pip

# 3. استنساخ المشروع (إذا لم يكن موجوداً)
if [ ! -d "al_mubarazi_system" ]; then
  echo "استنساخ مستودع المشروع..."
  git clone https://github.com/your_username/al_mubarazi_system.git
  cd al_mubarazi_system
else
  echo "المشروع موجود بالفعل. الانتقال إلى مجلد المشروع..."
  cd al_mubarazi_system
  git pull
fi

# 4. تثبيت المكتبات المطلوبة
echo "تثبيت مكتبات Python المطلوبة..."
pip install -r requirements.txt

# 5. إعداد ملف .env
if [ ! -f ".env" ]; then
  echo "إنشاء ملف .env من .env.example. يرجى تعديله ببياناتك."
  cp .env.example .env
  # فتح الملف للتعديل (يمكن للمستخدم تعديله يدوياً لاحقاً)
  # nano .env
else
  echo "ملف .env موجود بالفعل."
fi

# 6. تهيئة قاعدة البيانات
echo "تهيئة قاعدة البيانات..."
python -c "from database.crud import init_db; init_db()"

echo "\nتم إعداد النظام بنجاح!"
echo "الخطوات التالية:"
echo "1. قم بتعديل ملف .env وأضف TELEGRAM_BOT_TOKEN و ADMIN_CHAT_ID الخاص بك."
echo "2. لتشغيل البوت: python main.py"
