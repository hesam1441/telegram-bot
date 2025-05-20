import requests

BOT_TOKEN = "8120263843:AAFV8sLNCHEB2LVJJM5N8ASeYimqZq2mdvY"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"

response = requests.get(url)

if response.status_code == 200:
    print("✅ Webhook با موفقیت حذف شد.")
    print("پاسخ:", response.json())
else:
    print("❌ خطا در حذف Webhook")
    print("وضعیت:", response.status_code)
    print("پاسخ:", response.text)
