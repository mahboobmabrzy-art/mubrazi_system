#!/bin/bash
PID=$(pgrep -f "uvicorn app:app")
if [ -z "$PID" ]; then
    echo "⚠️ لا توجد عملية شغالة حالياً لخادم API."
else
    kill -9 $PID
    echo "🛑 تم إيقاف خادم API لنظام المبرزي بنجاح."
fi
