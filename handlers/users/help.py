import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import ChatType

from loader import dp, bot


@dp.message_handler(CommandHelp(), chat_type=ChatType.PRIVATE)
async def bot_help(message: types.Message):
    text = ("<b>Списък с команди: ",
            "/start - Започнете диалог",
            "/help - Извикай помощ",
            "/menu - Използвайте менюто на ботовете</b>")

    await message.answer("\n".join(text))

    await message.delete()
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, message.message_id + 1)
