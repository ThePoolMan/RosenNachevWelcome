from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Стартиране на бот"),
            types.BotCommand("help", "Покажи помощ"),
            types.BotCommand("menu", "Отворете менюто"),
        ]
    )
