import logging

from asyncio import sleep

from BD import bd

from Helpers.notify_sv import check_for_notification_sv
from Helpers.notify_nb import check_for_notification_nb

from aiogram import Bot

logger = logging.getLogger(__name__)


async def notify(bot: Bot):
    delay = 60 * 60
    while True:
        logger.info("notify")
        names_to_check, idts, notified_eps, _ = bd.select_notified_ep('nb')
        
        dict_name_url = check_for_notification_nb(names_to_check, idts, notified_eps)
        
        for k, v in dict_name_url.items():
            url, idt, notified_ep_ = v.split(",")

            pre_text = f"Episode {notified_ep_} is OUT\n{k}\n{url}"
            
            await bot.send_message(idt, pre_text)

            bd.update_notified_ep(idt, k, notified_ep_, 'nb')


        await sleep(delay)


async def notify_sv(bot: Bot):
    delay = 60 * 60

    while True:
        logger.info("notify sv")

        names_to_check, idts_, notified_eps, dub_or_sub = bd.select_notified_ep("sv")        

        dict_name_url = await check_for_notification_sv(names_to_check, idts_, notified_eps, dub_or_sub)

        for k, v in dict_name_url.items():
            url, idt, notified_ep_ = v.split(",")

            pre_text = f"Episode {notified_ep_} is OUT\n{k}\n{url}"

            await bot.send_message(idt, pre_text)

            bd.update_notified_ep(idt, k, notified_ep_, 'sv')

        await sleep(delay)
