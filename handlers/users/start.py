import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command
from aiogram.types import ChatType
from aiogram.dispatcher.filters import Text


from loader import dp, bot


@dp.message_handler(CommandStart(), chat_type=ChatType.PRIVATE)
async def bot_start(message: types.Message):
    print(message.from_user.username)
    print(message.from_user.id)
    await message.answer(f"<b>Приветствую👋, {message.from_user.full_name}!</b>")
    await message.answer("<b>Используй /menu для управления ботом</b>")

    await message.delete()
    await asyncio.sleep(10)

    await bot.delete_message(message.chat.id, message.message_id + 1)
    await bot.delete_message(message.chat.id, message.message_id + 2)


# # @dp.message_handler(Command("/start@RosenNachev_welcome_bot"))
# @dp.message_handler(Command('/start@RosenNachev_welcome_bot'), state='*')
# @dp.message_handler(Text(equals='/start@RosenNachev_welcome_bot', ignore_case=True), state='*')
# async def bot_start(message: types.Message):
#     response = await bot.get_updates()
#     for _ in response:
#         print(_)
#     for _ in response.pop():
#         print(_)
#     await message.reply(f"<b>{response}</b>")

    # await message.delete()
    # await asyncio.sleep(10)
    #
    # await bot.delete_message(message.chat.id, message.message_id + 1)
    # await bot.delete_message(message.chat.id, message.message_id + 2)

