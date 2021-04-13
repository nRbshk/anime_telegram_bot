import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

logger = logging.getLogger(__name__)



async def cmd_start(message: types.Message, state: FSMContext):
    logger.info("CMD start or help")
    await state.finish()
    text = []
    text.append("/cancel - Cancel last command\n")
    text.append("/add - Add anime to list\n")
    text.append("/show - Show anime by status\n")
    text.append("/set_time - Set time for last episode\n")
    text.append("/set_status - Set status for anime\n")
    text.append("/set_episode - Set episode for anime\n")
    text.append("/set_link_loc - Set link location for anime\n")
    await message.answer(
        "".join(text),
        reply_markup=types.ReplyKeyboardRemove()
    )

async def cmd_cancel(message: types.Message, state: FSMContext):
    logger.info("CMD cancel")
    await state.finish()
    await message.answer("Undo.", reply_markup=types.ReplyKeyboardRemove())



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_start, commands="help", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="undo", ignore_case=True), state="*")