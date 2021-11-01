import logging

from aiogram import Dispatcher

from data import config


async def on_startup_notify(dp: Dispatcher):
    for admin in config.ADMINS:
        try:
            pass
            await dp.bot.send_message(int(admin), "Стартиран бот")

        except Exception as err:
            logging.exception(err)
