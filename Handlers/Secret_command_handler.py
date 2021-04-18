import logging
from os import stat
from sqlite3.dbapi2 import Error

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from BD import bd




logger = logging.getLogger(__name__)

async def secret_command_start(message: types.Message):
    text = message.text.split(" ")
    cmd = text[0]

    idt = message.from_user.id
    name = text[1].replace("_", " ")
    episode = text[2]
    send = 0
    if cmd == '/secret_add':
        dub_or_sub = text[3]
        nb_or_sv = text[4]
        status = "inProgress"
        prepared_text = f"Anime {name} with episode {episode} added."
        send = bd.save_anime(idt, name, status, episode, dub_or_sub, nb_or_sv)

    elif cmd == '/secret_set_episode':
        bd.set_episode(idt, name, episode)
        prepared_text = f"Episode {episode} for anime {name} setted."
        send = 0
    
    if send == 0:
        await message.answer(prepared_text)
    elif send == 1:
        await message.answer("Error was ocured while inserting in bd.")
    elif send == 2:
        await message.answer("Anime already in your list.")
    



def register_handlers_secret_command(dp: Dispatcher):
    dp.register_message_handler(secret_command_start, commands=["secret_add", "secret_set_episode"], state="*")

