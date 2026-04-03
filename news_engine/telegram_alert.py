import requests

BOT_TOKEN = "8560045449:AAFAkW7cJ0Zhbf2O6ow0U90lZWSwzkAD858"
CHAT_ID = "5827865878"


def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)