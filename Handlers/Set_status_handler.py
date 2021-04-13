import logging


from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from BD import bd, available_status

class Set_status_handler(StatesGroup):

    name = State()
    status = State()



logger = logging.getLogger(__name__)

available_status = available_status[:-1]

async def set_time_start(message: types.Message):
    response = bd.show(message.from_user.id, 'All')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for r in response:
        kb.add(r[2])

    await message.answer('Choose anime.', reply_markup=kb)

    await Set_status_handler.name.set()

async def chosen_anime(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    await state.update_data(idt=message.from_user.id)
    
    name = message.text
    

    await state.update_data(name=name)


    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for k in available_status:
        kb.add(k)
        
    await Set_status_handler.status.set()

    await message.answer("Choose status", reply_markup=kb)

    

async def chosen_status(message: types.Message, state: FSMContext):
    logger.info("STATUS status")

    status = message.text

    if status not in available_status:
        message.answer("Use keyboard.")

    await state.update_data(status=status)

    user_data = await state.get_data()

    name = user_data['name']


    await update_in_bd(state)

    await message.answer(f"Status `{status}` for anime `{name}` updated.", reply_markup=types.ReplyKeyboardRemove())

    await state.finish()
    
async def update_in_bd(state: FSMContext):
    user_data = await state.get_data()

    idt = user_data['idt']
    name = user_data['name']
    status = user_data['status']

    bd.set_status(idt, name, status)

def register_handlers_set_status(dp: Dispatcher):
    dp.register_message_handler(set_time_start, commands="set_status", state="*")
    dp.register_message_handler(chosen_anime, state=Set_status_handler.name)
    dp.register_message_handler(chosen_status, state=Set_status_handler.status)
