
import os
import smtplib
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

# دریافت متغیرها از محیط
BOT_TOKEN = os.getenv("BOT_TOKEN")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)

# مراحل گفتگو
TEXT_CONTACT, ORDER = range(2)

# صفحه کلید اصلی
keyboard = [
    ["📞 تماس تلفنی", "💬 تماس متنی"],
    ["🛒 ثبت سفارش"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "به ربات ما خوش آمدید! لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup
    )

# تماس تلفنی
async def phone_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("برای تماس تلفنی با ما با این شماره تماس بگیرید:
📞 09125139013")

# شروع تماس متنی
async def text_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً پیام خود را وارد کنید تا برای ما ارسال شود:")
    return TEXT_CONTACT

# پردازش پیام تماس متنی
async def handle_text_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    subject = "تماس متنی از ربات تلگرام"
    send_email(subject, user_message)
    await update.message.reply_text("پیام شما با موفقیت ارسال شد.")
    return ConversationHandler.END

# شروع ثبت سفارش
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً جزئیات سفارش خود را وارد کنید:")
    return ORDER

# پردازش سفارش
async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    subject = "سفارش جدید از ربات تلگرام"
    send_email(subject, user_message)
    await update.message.reply_text("سفارش شما با موفقیت ثبت شد.")
    return ConversationHandler.END

# لغو عملیات
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END

# ارسال ایمیل
def send_email(subject, message):
    full_message = f"Subject: {subject}\n\n{message}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, full_message)
    except Exception as e:
        logging.error(f"خطا در ارسال ایمیل: {e}")

# راه‌اندازی ربات
if __name__ == "__main__":
    print("ربات داره شروع می‌کنه...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^💬 تماس متنی$"), text_contact),
            MessageHandler(filters.Regex("^🛒 ثبت سفارش$"), order),
        ],
        states={
            TEXT_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_contact)],
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^📞 تماس تلفنی$"), phone_call))
    app.add_handler(conv_handler)

    app.run_polling()
