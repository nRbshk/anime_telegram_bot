import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from helpers import *

from Handlers.Add_handler import register_handlers_add
from Handlers.Common_handler import register_handlers_common
from Handlers.Show_handler import register_handlers_show
from Handlers.Set_time_handler import register_handlers_set_time
from Handlers.Set_status_handler import register_handlers_set_status
from Handlers.Set_episode_handler import register_handlers_set_episode

logger = logging.getLogger(__name__)

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
        BotCommand(command='/watch', description="Not Implemented")
        # BotCommand(command='/watch', description="Watch anime with status inProgress")
    ]

    await bot.set_my_commands(commands)


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")


    bot = Bot(token=get_token())
    dp = Dispatcher(bot, storage=MemoryStorage())


    register_handlers_common(dp)
    register_handlers_add(dp)
    register_handlers_show(dp)
    register_handlers_set_time(dp)
    register_handlers_set_status(dp)
    register_handlers_set_episode(dp)


    await set_commands(bot)

    await dp.start_polling()