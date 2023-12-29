

def telegram_bot_send(token, chat_id, message):
    import telebot
    print(f"Sending message '{message}' to chat {chat_id}")
    telebot.TeleBot(token).send_message(chat_id, message)


