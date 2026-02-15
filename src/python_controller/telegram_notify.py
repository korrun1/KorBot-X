from telegram import Bot

def send_telegram_notification(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)
    print("Telegram notification sent: " + message)

if __name__ == "__main__":
    send_telegram_notification("7940972958:AAEcbg4qvcKgxzZQOgNEcmol8xaFgD0bpTw", "2013839088", "Test message from KorBot X")