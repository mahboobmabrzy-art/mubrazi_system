#!/bin/bash
PID=$(pgrep -f "modules/bot/telegram_bot.py")
if [ -z "$PID" ]; then
    echo "❌ بوت نظام المبرزي متوقف حالياً."
else
    echo "✅ بوت نظام المبرزي يعمل بنجاح (PID: $PID)."
fi
