
# 🤖 Telegram Bot for Contact and Orders

This is a simple Telegram bot written in Python that allows users to:

- 📞 Send a phone contact request
- 📝 Submit a message form (contact us)
- 📦 Place an order with form
- 📧 Emails the collected data to a specified recipient

The bot is designed to run continuously using services like [Render.com](https://render.com) or [PythonAnywhere](https://www.pythonanywhere.com/).

---

## 🚀 Features

- Interactive buttons for user actions
- Form data collected via chat
- Email notifications
- Compatible with Render.com deployment

---

## 🛠 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

This bot uses the following environment variables:

| Key             | Description                     |
|----------------|----------------------------------|
| `BOT_TOKEN`     | Telegram bot token              |
| `EMAIL_ADDRESS` | Gmail address to send from      |
| `EMAIL_PASSWORD`| Gmail app password              |
| `RECEIVER_EMAIL`| Email address to receive forms  |

> Set these in Render or your environment for security.

---

## ▶️ Running the Bot

To run locally:

```bash
python bot.py
```

To deploy on [Render](https://render.com):

1. Push this repo to GitHub.
2. Connect the repo to Render as a **Web Service**.
3. Set the environment variables in the **Environment tab**.
4. Use the following start command:

```bash
python bot.py
```

---

## 📬 Example Email Output

```text
[Contact Us Form]
Name: Ali
Phone: 0912XXXXXXX
Message: سلام، من سوالی دارم...

Message ID: 20250519202101
```

---

## 🔐 Security Note

Never hard-code tokens or passwords. Always use environment variables to store credentials.

---

## 📧 Support

If you need help setting up this bot, feel free to reach out!

---

**Created by arcatav** | 2025
