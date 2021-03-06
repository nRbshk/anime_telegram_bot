import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Helpers.helpers import get_token

from Handlers.Add_handler import register_handlers_add
from Handlers.Common_handler import register_handlers_common
from Handlers.Show_handler import register_handlers_show
from Handlers.Set_time_handler import register_handlers_set_time
from Handlers.Set_status_handler import register_handlers_set_status
from Handlers.Set_episode_handler import register_handlers_set_episode
from Handlers.Set_link_loc_handler import register_handlers_set_link_loc
from Handlers.Watch_handler import register_handlers_watch
from Handlers.Secret_command_handler import register_handlers_secret_command

from Services.Notify import notify, notify_sv

from asyncio import create_task

logger = logging.getLogger(__name__)

proxy_url = ""

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/add', description="Add anime to list"),
        BotCommand(command='/help', description="Show help"),
        BotCommand(command='/start', description="Show help"),
        BotCommand(command='/show', description="Show anime by status"),
        BotCommand(command='/cancel', description='Cancel last command'),
        BotCommand(command='/set_time', description='Set time for last episode'),
        BotCommand(command='/set_status', description="Set status for anime"),
        BotCommand(command='/set_episode', description="Set episode for anime"),
        BotCommand(command='/set_link_loc', description="Set link location for anime"),
        BotCommand(command='/watch', description="Sending link for last episode if exists. Available only for link location = 'sv'"),
    ]

    await bot.set_my_commands(commands)


async def start():
    logging.basicConfig(
        filename='log.log',
        filemode='w',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt='%d-%m-%y %H:%M:%S'
    )
    logger.info("Starting bot")


    bot = Bot(token=get_token(), proxy=proxy_url)
    dp = Dispatcher(bot, storage=MemoryStorage())


    register_handlers_common(dp)
    register_handlers_add(dp)
    register_handlers_show(dp)
    register_handlers_set_time(dp)
    register_handlers_set_status(dp)
    register_handlers_set_episode(dp)
    register_handlers_set_link_loc(dp)
    register_handlers_watch(dp)
    register_handlers_secret_command(dp)

    create_task(notify(bot))
    create_task(notify_sv(bot))

    await set_commands(bot)


    await dp.start_polling(timeout=600)
