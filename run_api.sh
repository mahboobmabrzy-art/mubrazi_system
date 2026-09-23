#!/bin/bash
cd ~/mubrazi_system
echo "جاري بدء تشغيل خادم FastAPI المحلي لنظام المبرزي للبصريات والسمعيات..."
python -m uvicorn app:app --host 0.0.0.0 --port 8000
