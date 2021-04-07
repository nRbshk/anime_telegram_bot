import telebot

bot = telebot.TeleBot("")
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "message received.")
    if message.text == "Hello":
        bot.send_message(message.from_user.id, "POKA")




def get_token(fn: str = "token.token"):
    f = open(fn, 'r')
    token = f.readline()
    f.close()
    return token

if __name__ == '__main__':
    print('Running bot.')
    token = get_token()
    bot.token = token
    bot.polling(none_stop=False, interval=0)


