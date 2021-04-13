import logging


from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from BD import bd, available_link_locs

class Set_link_loc_handler(StatesGroup):

    name = State()
    link_loc = State()



logger = logging.getLogger(__name__)


async def set_link_loc_start(message: types.Message):
    response = bd.show(message.from_user.id, 'All')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for r in response:
        kb.add(r[2])

    await message.answer('Choose anime.', reply_markup=kb)

    await Set_link_loc_handler.name.set()

async def chosen_anime(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    await state.update_data(idt=message.from_user.id)
    
    name = message.text
    

    await state.update_data(name=name)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for l in available_link_locs:
        kb.add(l)
    await message.answer("Choose link location", reply_markup=kb)

    await Set_link_loc_handler.link_loc.set()
    

async def chosen_link_loc(message: types.Message, state: FSMContext):
    logger.info("STATUS chosen_link_loc")

    if message.text not in available_link_locs:
        await message.answer("Use keyboard.")
        return


    link_loc = message.text
    user_data = await state.get_data()
    name = user_data['name']

    await state.update_data(link_loc=link_loc)

    await update_in_bd(state)

    await message.answer(f"Link location {link_loc} for anime\n{name}\n was setted.", reply_markup=types.ReplyKeyboardRemove())

    await state.finish()
    
async def update_in_bd(state: FSMContext):
    user_data = await state.get_data()

    idt = user_data['idt']
    name = user_data['name']
    link_loc = user_data['link_loc']
    bd.set_link_loc(idt, name, link_loc)

def register_handlers_set_link_loc(dp: Dispatcher):
    dp.register_message_handler(set_link_loc_start, commands="set_link_loc", state="*")
    dp.register_message_handler(chosen_anime, state=Set_link_loc_handler.name)
    dp.register_message_handler(chosen_link_loc, state=Set_link_loc_handler.link_loc)
