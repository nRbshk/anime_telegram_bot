import logging
from typing import Set

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup

from BD import bd

class Set_episode_handler(StatesGroup):

    name = State()
    episode = State()



logger = logging.getLogger(__name__)


async def set_episode_start(message: types.Message):
    response = bd.show(message.from_user.id, 'inProgress')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for r in response:
        kb.add(r[2])

    await message.answer('Choose anime.', reply_markup=kb)

    await Set_episode_handler.name.set()

async def chosen_anime(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    await state.update_data(idt=message.from_user.id)
    
    name = message.text
    

    await state.update_data(name=name)


    await message.answer("Type episode", reply_markup=types.ReplyKeyboardRemove())

    await Set_episode_handler.episode.set()
    

async def chosen_episode(message: types.Message, state: FSMContext):
    logger.info("STATUS episode")

    episode = message.text
    user_data = await state.get_data()
    name = user_data['name']

    await state.update_data(episode=episode)

    await update_in_bd(state)

    await message.answer(f"Episode {episode} for anime {name} setted.")

    await state.finish()
    
async def update_in_bd(state: FSMContext):
    user_data = await state.get_data()

    idt = user_data['idt']
    name = user_data['name']
    episode = user_data['episode']

    logger.info(f"UPDATE in bd name={name} episode={episode}")

    bd.set_episode(idt, name, episode)

def register_handlers_set_episode(dp: Dispatcher):
    dp.register_message_handler(set_episode_start, commands="set_episode", state="*")
    dp.register_message_handler(chosen_anime, state=Set_episode_handler.name)
    dp.register_message_handler(chosen_episode, state=Set_episode_handler.episode)
