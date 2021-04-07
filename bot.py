from telebot import TeleBot
bot = TeleBot("")
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "message received.")
    if message.text == "Hello":
        bot.send_message(message.from_user.id, "POKA")
