import logging


from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import user
from requests.api import get

from BD import bd, available_link_locs
from Helpers.notify_sv import get_episodes_sv, get_id_sv, get_link_sv


class Watch_handler(StatesGroup):

    name = State()



logger = logging.getLogger(__name__)


async def watch_start(message: types.Message, state: FSMContext):
    logger.info("START watch start")
    response = bd.show(message.from_user.id, 'All')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    resp = []
    for r in response:
        if r[-1] == 'sv':
            kb.add(r[2])
            resp.append(r)

    del response
    await state.update_data(resp=resp)
    await message.answer('Choose anime.', reply_markup=kb)

    await Watch_handler.name.set()

async def chosen_anime(message: types.Message, state: FSMContext):
    logger.info("STATUS name")
    await state.update_data(idt=message.from_user.id)
    
    name = message.text
    

    await state.update_data(name=name)

    user_data = await state.get_data()

    resp = user_data['resp']

    # last_episode = 0
    # for r in resp:
    #     if name == r[2]:
    #         last_episode = r[4]
    
    anime_id = get_id_sv(name)
    if anime_id is None:
        await message.answer(f"No anime with name {name}", reply_markup=types.ReplyKeyboardRemove())
    r_episodes = get_episodes_sv(anime_id)
    if r_episodes is None:
        await message.answer(f"Anime {name} is not out", reply_markup=types.ReplyKeyboardRemove())

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
