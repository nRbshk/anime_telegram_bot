import logging


from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from BD import bd, available_dub_sub, DB_positions
from Helpers.notify_sv import get_episodes_sv, get_id_sv


class Watch_handler(StatesGroup):

    name = State()
    dub_or_sub = State()



logger = logging.getLogger(__name__)


async def watch_start(message: types.Message):
    logger.info("START watch start")
    response = bd.show(message.from_user.id, 'All')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for r in response:
        if r[DB_positions.link_loc_position.value] == 'sv':
            kb.add(r[DB_positions.name_position.value])

    del response
    await message.answer('Choose anime.', reply_markup=kb)

    await Watch_handler.name.set()

async def chosen_anime(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    await state.update_data(idt=message.from_user.id)
    
    name = message.text
    

    await state.update_data(name=name)


    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for ds in available_dub_sub:
        kb.add(ds)
    
    await message.answer("Choose dub or sub", reply_markup=kb)

    await Watch_handler.dub_or_sub.set()
    
async def chosen_dub_sub(message: types.Message, state: FSMContext):
    ds = message.text
    if ds not in available_dub_sub:
        message.answer("Use keyboard")
        return
    
    user_data = await state.get_data()
    name = user_data['name']

    anime_id = get_id_sv(name)
    if anime_id is None:
        await message.answer(f"No anime with name {name}", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    r_episodes = get_episodes_sv(anime_id, dub_or_sub=ds)
    if r_episodes is None:
        await message.answer(f"Anime {name} is not out", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return

    prep_data = [f"{name}\n\n"]
    for rep in r_episodes:
        link = rep['embed']
        episode = rep['episode_count']
        prep_data.append(f"Episode {episode}\n{link}\n")

    await message.answer("".join(prep_data), reply_markup=types.ReplyKeyboardRemove())
 
    await state.finish()

def register_handlers_watch(dp: Dispatcher):
    dp.register_message_handler(watch_start, commands="watch", state="*")
    dp.register_message_handler(chosen_anime, state=Watch_handler.name)
    dp.register_message_handler(chosen_dub_sub, state=Watch_handler.dub_or_sub)
