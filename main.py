import telebot




@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # if message.rom_user.id == 900530539:
    if message.text == "Hello":
        bot.send_message(message.from_user.id, "POKA")



bot.polling(none_stop=True, interval=0)

