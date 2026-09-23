import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from config import Config
from database.crud import init_db, SessionLocal, get_customer_by_phone, create_customer
from modules.accounting.services import AccountingService
from modules.medical.services import MedicalService
from modules.marketing.services import MarketingService

# إعداد التسجيل (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# حالات المحادثة (Conversation States)
CHOOSING, TYPING_REPLY, PHOTO_UPLOAD = range(3)

# لوحة المفاتيح الرئيسية
main_keyboard = [['المحاسبة 💰', 'الجانب الطبي 🏥'], ['التسويق 📢', 'سجل العملاء 👤']]
markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=False, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في نظام المبرزي المتكامل. اختر القسم المطلوب:",
        reply_markup=markup
    )

async def accounting_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    report = AccountingService.get_financial_report(db)
    db.close()
    
    text = (f"📊 التقرير المالي الموجز:\n"
            f"💰 إجمالي المبيعات: {report['total_sales']:.2f}\n"
            f"📈 إجمالي الأرباح: {report['total_profit']:.2f}\n"
            f"🎯 هامش الربح: {report['net_margin']:.1f}%")
    await update.message.reply_text(text)

async def medical_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏥 قسم الفحوصات الطبية: (قيد التطوير للربط مع النماذج)")

async def marketing_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📢 قسم التسويق: يمكنك إرسال العروض للعملاء من هنا.")

async def customer_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 ابحث عن عميل برقم الهاتف:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'المحاسبة 💰':
        await accounting_menu(update, context)
    elif text == 'الجانب الطبي 🏥':
        await medical_menu(update, context)
    elif text == 'التسويق 📢':
        await marketing_menu(update, context)
    elif text == 'سجل العملاء 👤':
        await customer_search(update, context)
    else:
        # معالجة البحث عن عميل إذا كان النص رقم هاتف
        if text.isdigit():
            db = SessionLocal()
            customer = get_customer_by_phone(db, text)
            if customer:
                res = f"✅ عميل موجود: {customer.name}\nعدد الفواتير: {len(customer.invoices)}"
            else:
                res = "❌ العميل غير موجود في النظام."
            db.close()
            await update.message.reply_text(res)

def main():
    # تهيئة قاعدة البيانات والمجلدات
    init_db()
    Config.init_app()
    
    # بناء التطبيق
    if not Config.TELEGRAM_BOT_TOKEN:
        print("خطأ: TELEGRAM_BOT_TOKEN غير موجود في ملف .env")
        return

    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("النظام يعمل الآن... اضغط Ctrl+C للإيقاف")
    app.run_polling()

if __name__ == '__main__':
    main()
