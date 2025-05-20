print("ربات داره شروع می‌کنه...")

import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# --- Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Config from env
BOT_TOKEN = os.getenv("BOT_TOKEN")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# --- States
CALL_NAME, CALL_PHONE, CALL_MESSAGE = range(3)
ORDER_NAME, ORDER_CONTACT, ORDER_PRODUCT, ORDER_QUANTITY = range(4)

# --- Main Menu
main_keyboard = [
    ["📞 تماس متنی", "🛒 ثبت سفارش"],
    ["📱 تماس تلفنی"]
]
main_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_markup
    )

# تماس متنی
async def call_us_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا نام خود را وارد کنید:")
    return CALL_NAME

async def call_us_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['call_name'] = update.message.text
    await update.message.reply_text("شماره تماس خود را وارد کنید:")
    return CALL_PHONE

async def call_us_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['call_phone'] = update.message.text
    await update.message.reply_text("پیام خود را وارد کنید:")
    return CALL_MESSAGE

async def call_us_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['call_message'] = update.message.text

    subject = "درخواست تماس متنی"
    body = (
        f"نام: {context.user_data['call_name']}\n"
        f"شماره تماس: {context.user_data['call_phone']}\n"
        f"پیام: {context.user_data['call_message']}"
    )
    send_email(subject, body)

    await update.message.reply_text("پیام شما ثبت شد. با تشکر!", reply_markup=main_markup)
    return ConversationHandler.END

# سفارش
async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا نام خود را وارد کنید:")
    return ORDER_NAME

async def order_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_name'] = update.message.text
    await update.message.reply_text("اطلاعات تماس خود را وارد کنید:")
    return ORDER_CONTACT

async def order_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_contact'] = update.message.text
    await update.message.reply_text("نام کالا را وارد کنید:")
    return ORDER_PRODUCT

async def order_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_product'] = update.message.text
    await update.message.reply_text("مقدار را وارد کنید:")
    return ORDER_QUANTITY

async def order_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_quantity'] = update.message.text

    subject = "درخواست ثبت سفارش"
    body = (
        f"نام: {context.user_data['order_name']}\n"
        f"اطلاعات تماس: {context.user_data['order_contact']}\n"
        f"نام کالا: {context.user_data['order_product']}\n"
        f"مقدار: {context.user_data['order_quantity']}"
    )
    send_email(subject, body)

    await update.message.reply_text("سفارش شما ثبت شد.", reply_markup=main_markup)
    return ConversationHandler.END

# تماس تلفنی
async def phone_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("شماره تماس مدیریت: 09125139013")

# لغو
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات لغو شد.", reply_markup=main_markup)
    return ConversationHandler.END

# ارسال ایمیل
def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        logging.info("Email sent")
    except Exception as e:
        logging.error(f"Email error: {e}")

# main
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_call = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^📞 تماس متنی$'), call_us_start)],
        states={
            CALL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, call_us_name)],
            CALL_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, call_us_phone)],
            CALL_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, call_us_message)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    conv_order = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🛒 ثبت سفارش$'), order_start)],
        states={
            ORDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_name)],
            ORDER_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_contact)],
            ORDER_PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_product)],
            ORDER_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_quantity)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_call)
    application.add_handler(conv_order)
    application.add_handler(MessageHandler(filters.Regex('^📱 تماس تلفنی$'), phone_contact))

    application.run_polling()

if __name__ == '__main__':
    main()
