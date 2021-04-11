import logging
from typing import Set

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup

from BD import BD, bd, available_status

class Set_time_handler(StatesGroup):

    name = State()
    time = State()



logger = logging.getLogger(__name__)


async def set_time_start(message: types.Message):
    response = bd.show(message.from_user.id, 'inProgress')

    kb = types.ReplyKeyboardMarkup()
    for r in response:
        kb.add(r[2])

    await message.answer('Choose anime.', reply_markup=kb)

    await Set_time_handler.name.set()

async def chosen_anime(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    await state.update_data(idt=message.from_user.id)
    
    name = message.text
    

    await state.update_data(name=name)


    await message.answer("Enter time in format 00 00", reply_markup=types.ReplyKeyboardRemove())

    await Set_time_handler.time.set()
    

async def chosen_time(message: types.Message, state: FSMContext):
    logger.info("STATUS time")

    time = message.text
    user_data = await state.get_data()
    name = user_data['name']

    await state.update_data(time=time)

    await update_in_bd(state)

    await message.answer(f"Time {time} for anime {name} was setted.")
    
async def update_in_bd(state: FSMContext):
    user_data = await state.get_data()

    idt = user_data['idt']
    name = user_data['name']
    time = user_data['time']

    bd.set_time(idt, name, time)

def register_handlers_set_time(dp: Dispatcher):
    dp.register_message_handler(set_time_start, commands="set_time", state="*")
    dp.register_message_handler(chosen_anime, state=Set_time_handler.name)
    dp.register_message_handler(chosen_time, state=Set_time_handler.time)
