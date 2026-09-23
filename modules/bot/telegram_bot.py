import sys
import os
import telebot

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import TELEGRAM_BOT_TOKEN
from database.models import Customer, Invoice
from database.init_db import engine
from sqlalchemy.orm import sessionmaker
from modules.accounting.invoice_formatter import InvoiceFormatter

Session = sessionmaker(bind=engine)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE" else None

def get_db_session():
    return Session()

if bot:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        welcome_text = (
            "👓👂 **نظام المبرزي للبصريات والسمعيات**\n"
            "مرحباً بك في بوت إدارة المبيعات والحسابات (`@MubraziCounter_bot`).\n\n"
            "📋 **الأوامر المتاحة**:\n"
            "• `/stats` - عرض الإحصائيات العامة\n"
            "• `/latest` - عرض آخر فاتورة مسجلة\n"
            "• `/search <الاسم أو الهاتف>` - البحث عن عميل\n"
            "• `/help` - عرض قائمة المساعدة"
        )
        bot.reply_to(message, welcome_text, parse_mode="Markdown")

    @bot.message_handler(commands=['stats'])
    def send_stats(message):
        session = get_db_session()
        try:
            customer_count = session.query(Customer).count()
            invoice_count = session.query(Invoice).count()
            stats_text = (
                "📊 **إحصائيات نظام المبرزي**:\n"
                f"• إجمالي العملاء: `{customer_count}`\n"
                f"• إجمالي الفواتير: `{invoice_count}`"
            )
            bot.reply_to(message, stats_text, parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {str(e)}")
        finally:
            session.close()

    @bot.message_handler(commands=['latest'])
    def send_latest_invoice(message):
        session = get_db_session()
        try:
            latest_inv = session.query(Invoice).order_by(Invoice.id.desc()).first()
            if not latest_inv:
                bot.reply_to(message, "لا توجد فواتير مسجلة حالياً.")
                return
            
            customer = session.query(Customer).filter_by(id=latest_inv.customer_id).first()
            customer_name = customer.name if customer else "غير معروف"
            customer_phone = customer.phone if customer else "غير متوفر"

            formatted_invoice = InvoiceFormatter.format_invoice_text(
                invoice_number=latest_inv.invoice_number,
                customer_name=customer_name,
                customer_phone=customer_phone,
                item_name=latest_inv.item_name,
                item_type=latest_inv.item_type,
                details_table=[{"desc": latest_inv.item_name, "price": latest_inv.total_amount}],
                total_amount=latest_inv.total_amount,
                paid_amount=latest_inv.paid_amount
            )
            bot.reply_to(message, f"```\n{formatted_invoice}\n```", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ أثناء جلب الفاتورة: {str(e)}")
        finally:
            session.close()

    @bot.message_handler(commands=['search'])
    def search_customer(message):
        session = get_db_session()
        try:
            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                bot.reply_to(message, "يرجى إدخال اسم العميل أو رقم الهاتف بعد الأمر. مثال:\n`/search عميل`", parse_mode="Markdown")
                return
            
            query_str = args[1].strip()
            customers = session.query(Customer).filter(
                (Customer.name.like(f"%{query_str}%")) | (Customer.phone.like(f"%{query_str}%"))
            ).all()

            if not customers:
                bot.reply_to(message, f"لم يتم العثور على أي نتائج تطابق: `{query_str}`", parse_mode="Markdown")
                return

            res = ["🔍 **نتائج البحث في نظام المبرزي:**\n"]
            for c in customers:
                res.append(f"• **الاسم**: {c.name} | **الهاتف**: `{c.phone}` | **النوع**: {c.customer_type}")
            
            bot.reply_to(message, "\n".join(res), parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ أثناء البحث: {str(e)}")
        finally:
            session.close()

def start_bot():
    if not bot:
        print("تنبيه: يلزم ضبط TELEGRAM_BOT_TOKEN داخل ملف .env لتشغيل الاتصال الحي.")
        return
    print("جاري تشغيل بوت التليجرام MubraziCounter_bot...")
    bot.infinity_polling()

if __name__ == "__main__":
    start_bot()
