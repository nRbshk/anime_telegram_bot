import logging

from asyncio import sleep

from helpers import check_page
from BD import bd


from aiogram import Bot

logger = logging.getLogger(__name__)

async def notify(bot: Bot):
    delay = 60
    while True:
        logger.info("notify")
        names_to_check, idts = bd.select_notify("False")
        
        dict_name_url = check_page(names_to_check, idts)
        
        for k, v in dict_name_url.items():
            url, idt = v.split(",")
            pre_text = f"New episode of anime `{k}` is out\n{url}"
            
            await bot.send_message(idt, pre_text)

            bd.update_notify(idt, k, "True")


        await sleep(delay)


        

