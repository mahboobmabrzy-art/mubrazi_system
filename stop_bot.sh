#!/bin/bash
PID=$(pgrep -f "modules/bot/telegram_bot.py")
if [ -z "$PID" ]; then
    echo "⚠️ لا توجد عملية شغال حالياً للبوت."
else
    kill -9 $PID
    echo "🛑 تم إيقاف بوت نظام المبرزي بنجاح."
fi
