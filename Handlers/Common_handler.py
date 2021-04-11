import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

logger = logging.getLogger(__name__)



async def cmd_start(message: types.Message, state: FSMContext):
    logger.info("CMD start or help")
    await state.finish()
    text = []
    text.append("/add - Add anime to list\n")
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