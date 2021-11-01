import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ChatType


from loader import dp, bot


@dp.message_handler(CommandStart(), chat_type=ChatType.PRIVATE)
async def bot_start(message: types.Message):
    print(message.from_user.username)
    print(message.from_user.id)
    await message.answer(f"<b>Здравейте👋, {message.from_user.full_name}!</b>")
    await message.answer("<b>Използвайте /menu за управление на бота</b>")

    await message.delete()
    await asyncio.sleep(10)

    await bot.delete_message(message.chat.id, message.message_id + 1)
    await bot.delete_message(message.chat.id, message.message_id + 2)
