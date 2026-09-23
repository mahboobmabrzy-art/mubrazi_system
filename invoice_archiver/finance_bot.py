from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
TOKEN = '8375835755:AAHEFruDL5U7oPBowWM7Evnc5s2eKbf3PIU'
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ تم ربط النظام المالي بنجاح! بانتظار أوامر تحليل USDT.')
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    print('🚀 البوت يعمل الآن... اذهب إلى تلجرام')
    app.run_polling()
