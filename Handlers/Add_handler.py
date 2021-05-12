import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from DB.DB import DB, db, available_status, available_dub_sub
available_status = available_status[:-1]

logger = logging.getLogger(__name__)


class Add_handler(StatesGroup):

    name = State()
    dub_or_sub = State()
    status = State()
    episode = State()



async def add_start(message: types.Message):
    await message.answer("Type name.")
    await Add_handler.name.set()


async def anime_name_chosen(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    
    await state.update_data(chosen_name=message.text)
    await state.update_data(idt=message.from_user.id)
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for ds in available_dub_sub:
        kb.add(ds)
    
    await message.answer("Choose dub or sub", reply_markup=kb)

    await Add_handler.dub_or_sub.set()


async def anime_dub_sub_chosen(message: types.Message, state: FSMContext):
    logger.info("STATUS dub_sub")

    ds = message.text
    if ds not in available_dub_sub:
        await message.answer("Use keyboard.")
        return
    
    await state.update_data(dub_or_sub=ds)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for status in available_status:
        kb.add(status)


    await message.answer("Choose status.", reply_markup=kb)

    await Add_handler.status.set()
    
async def anime_status_chosen(message: types.Message, state: FSMContext):
    logger.info("STATUS status")

    if message.text not in available_status:
        await message.answer("Use keyboard.")
        return

    await state.update_data(status=message.text)

    if message.text == "inProgress":
        await message.answer("Enter episode.", reply_markup=types.ReplyKeyboardRemove())
        await Add_handler.episode.set()

    else:
        await state.update_data(episode=0)

        await insert_in_db(db, state)
        
        user_data = await state.get_data()
        await message.answer(f"Anime `{user_data['chosen_name']}` with status `{user_data['status']}` added.", reply_markup=types.ReplyKeyboardRemove())
        
        await state.finish()


async def anime_episode_chosen(message: types.Message, state: FSMContext):
    logger.info("STATUS episode")
    await state.update_data(episode=message.text)
    
    user_data = await state.get_data()
    await insert_in_db(db, state)
    
    await message.answer(f"Anime `{user_data['chosen_name']}` with status `{user_data['status']}` added.", reply_markup=types.ReplyKeyboardRemove())

    
    await state.finish()



async def insert_in_bd(db: DB, state: FSMContext):
    user_data = await state.get_data()
    idt = user_data['idt']
    name = user_data['chosen_name']
    status = user_data['status']
    ep = user_data['episode']
    ds = user_data['dub_or_sub']
    if not db.save_anime(idt, name, status, ep, ds):
        logger.info(f"insert in BD with data name={name} status={status} episode={ep} dub_or_sub={ds}")
    else:
        logger.error(f'Error when insert in BD')



def register_handlers_add(dp: Dispatcher):
    dp.register_message_handler(add_start, commands="add", state="*")
    dp.register_message_handler(anime_name_chosen, state=Add_handler.name)
    dp.register_message_handler(anime_dub_sub_chosen, state=Add_handler.dub_or_sub)
    dp.register_message_handler(anime_status_chosen, state=Add_handler.status)
    dp.register_message_handler(anime_episode_chosen, state=Add_handler.episode)
