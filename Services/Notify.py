import logging

from asyncio import sleep

from helpers import check_page
from BD import bd


from aiogram import Bot

logger = logging.getLogger(__name__)

async def notify(bot: Bot):
    delay = 60 * 60
    while True:
        logger.info("notify")
        names_to_check, idts, notified_ep = bd.select_notified_ep()
        
        dict_name_url = check_page(names_to_check, idts, notified_ep)
        
        for k, v in dict_name_url.items():
            url, idt, notified_ep_ = v.split(",")

            print(url ,idt, notified_ep_)
            pre_text = f"Episode {notified_ep_} of anime {k} is out\n{url}"
            
            await bot.send_message(idt, pre_text)

            bd.update_notified_ep(idt, k, notified_ep_)


        await sleep(delay)


        

