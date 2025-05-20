import logging
import smtplib
import ssl
import uuid
import os
from email.message import EmailMessage
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# متغیرها از محیط خوانده می‌شن
BOT_TOKEN = os.environ["BOT_TOKEN"]
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

CHOOSING, TYPING = range(2)
user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton("تماس با ما", callback_data='contact')],
        [InlineKeyboardButton("تماس تلفنی", callback_data='call')],
        [InlineKeyboardButton("ثبت سفارش", callback_data='order')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=reply_markup)
    return CHOOSING

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data_store[user_id] = {"choice": query.data}

    if query.data == 'call':
        await query.edit_message_text(text="برای تماس تلفنی با ما با این شماره تماس بگیرید:\n📞 0912-123-4567")
        return ConversationHandler.END
    else:
        prompt = "لطفاً پیام خود را بنویسید:" if query.data == 'contact' else "لطفاً جزئیات سفارش خود را وارد کنید:"
        await query.edit_message_text(text=prompt)
        return TYPING

async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    user_input = update.message.text
    choice = user_data_store[user_id]["choice"]
    unique_id = str(uuid.uuid4())[:8]

    subject_map = {
        "contact": "تماس با ما",
        "order": "ثبت سفارش"
    }

    subject = f"{subject_map.get(choice, 'درخواست')} - {unique_id}"
    body = f"پیام از: @{update.message.from_user.username or 'ندارد'}\n\nمتن پیام:\n{user_input}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(body)

    try:
        context_ssl = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context_ssl) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        await update.message.reply_text("✅ پیام شما با موفقیت ارسال شد.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        await update.message.reply_text("❌ ارسال پیام با مشکل مواجه شد.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("لغو شد.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [CallbackQueryHandler(button)],
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
