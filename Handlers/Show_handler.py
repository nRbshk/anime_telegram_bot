import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from BD.BD import BD, bd, available_status, DB_positions

class Show_handler(StatesGroup):

    status = State()



logger = logging.getLogger(__name__)


async def show_start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for status in available_status:
        kb.add(status)
    await message.answer("Choose status.", reply_markup=kb)
    await Show_handler.status.set()

async def chosen_status(message: types.Message, state: FSMContext):
    logger.info("STATUS status")
    await state.update_data(idt=message.from_user.id)
    
    status = message.text
    
    if status not in available_status:
        await message.answer("Use keyboard.")

    await state.update_data(status=message.text)
    response = await select_from_bd(bd, state)


    if response == []:
        await message.answer("List is empty.", reply_markup=types.ReplyKeyboardRemove())
    else:
        text = []
        for r in response:
            tmp = f"{r[DB_positions.name_position.value]}\nLast episode viewed: {r[DB_positions.episode_position.value]} / {r[DB_positions.notified_ep_position.value]}\nTime: {r[DB_positions.time_position.value]}\n\n"
            text.append(tmp)

        await message.answer("".join(text), reply_markup=types.ReplyKeyboardRemove())

    await state.finish()
    
async def select_from_bd(bd: BD, state: FSMContext):
    user_data = await state.get_data()
    idt = user_data['idt']
    status = user_data['status']

    logger.info(f"SELECT from bd status={status}")
    return bd.show(idt, status)



    


def register_handlers_show(dp: Dispatcher):
    dp.register_message_handler(show_start, commands="show", state="*")
    dp.register_message_handler(chosen_status, state=Show_handler.status)
