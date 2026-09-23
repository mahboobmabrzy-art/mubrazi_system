import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# تحميل متغيرات ملف .env تلقائياً
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/mubrazi_database.db")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "creds.json")

DATABASE_URL = Config.DATABASE_URL
TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
GOOGLE_SHEETS_CREDENTIALS_PATH = Config.GOOGLE_SHEETS_CREDENTIALS_PATH
