#!/bin/bash
PID=$(pgrep -f "uvicorn app:app")
if [ -z "$PID" ]; then
    echo "❌ خادم API لنظام المبرزي متوقف حالياً."
else
    echo "✅ خادم API لنظام المبرزي يعمل بنجاح (PID: $PID)."
fi
