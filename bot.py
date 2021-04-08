from telebot import TeleBot
from services.Action_factory import Action_factory
from services.BD import BD
from services.helpers import *


bot = TeleBot("")
factory = Action_factory(bot, BD())

# Переделать ЭКШОНЫ
# me: /start
# bot: Enter command
# me: /add
# bot: Enter name
# me: Naruto
# bot: Enter status
# me: done, isWatching, end

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "message received.")
    idt = message.from_user.id
    cmd, params = get_cmd_params(message.text, idt)
    print(params)
    action = factory.create_action(cmd)

    if action is None:
        bot.send_message(message.from_user.id, "Command not found.")
    else:
        action.handler(*params)
        del action


def start():
    print('Running bot.')

    bot.token = get_token()
    bot.polling(none_stop=False, interval=0)
