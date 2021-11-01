import asyncio
from datetime import datetime
from typing import Union
from loguru import logger

from aiogram.utils.exceptions import MessageToDeleteNotFound, ChatNotFound
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, ChatType

from keyboards.inline.menu_keyboards import *
from utils.permissions import *
from utils.db_api import db
from data import config

from loader import dp, bot

logger.add("INFO.log", format="{time} {level} {message}", level="INFO", rotation="1000 KB", compression="zip")

DELAY_DELETE_MESSAGE = 25
members = {}
flags = {'flag': True}


@dp.message_handler(content_types=['left_chat_member'])
async def left_member(message):
    if message.left_chat_member.id == 2008419805:
        all_chats = db.select_data_db("rosennachev_welcome_bot", "chats")
        for _ in all_chats:
            if message.chat.id == _[1]:
                db.delete_data_db("rosennachev_welcome_bot", "chats", f"chat_id = '{message.chat.id}'",
                                  "delete_records")
                logger.info(f"User: {message.from_user.username}, Action: delete chat")


@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message):
    if not str(message.from_user.id) in config.ADMINS:
        await bot.leave_chat(message.chat.id)
        logger.error(f"Please change anonymous rights for administrator or you are not administrator")
        return

    # для управления удаления сообщений
    user_join_message_id = message.message_id
    # получаем объект юзера
    user = message.new_chat_members[len(message.new_chat_members) - 1]

    if user.id == 2008419805:
        response = await bot.get_updates()
        pop_request = response.pop()
        try:
            chat_id = pop_request.message.chat.id
            chat_title = pop_request.message.chat.title
        except:
            chat_id = pop_request.my_chat_member.chat.id
            chat_title = pop_request.my_chat_member.chat.title
        now_time = datetime.now()
        db.insert_user_into_db("rosennachev_welcome_bot", "chats", chat_id, now_time, chat_title)
        logger.info(f"User: {message.from_user.username}, Action: add chat")

        await asyncio.sleep(120)
        try:
            await bot.delete_message(message.chat.id, user_join_message_id)
            await bot.delete_message(message.chat.id, user_join_message_id + 1)
        except:
            logger.error(f"Error delete message")
        return

    flags.update(flag=True)

    new_members_permissions = set_new_user_permissions()
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user.id,
        permissions=new_members_permissions,
    )

    await message.reply(
        (
            f"{user.get_mention(as_html=True)}, <b>Добре дошли в чата!\n"
            "Потвърдете, че не сте бот, като щракнете върху един от бутоните по-долу\n"
            "ВРЕМЕ ЗА ОТГОВОР 30 СЕКУНДИ!</b>\n"

        ),
        reply_markup=generate_confirm_markup(user.id, user_join_message_id)
    )
    logger.info(f"User: {user.username}, has join in chat")
    await asyncio.sleep(25)

    if flags.get('flag'):
        try:
            await bot.delete_message(message.chat.id, user_join_message_id)
            await bot.delete_message(message.chat.id, user_join_message_id + 1)
        except MessageToDeleteNotFound:
            print("I get error: MessageToDeleteNotFound")
        await message.chat.kick(user.id)


# Хендлер на команду /menu
@dp.message_handler(Command("menu"), chat_type=ChatType.PRIVATE)
async def show_menu(message: types.Message):
    await message.delete()
    if str(message.from_user.id) in config.ADMINS:
        await list_menu(message)


# Список кнопок меню
async def list_menu(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await menu_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("<b>🗂Меню</b>", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text="<b>🗂Меню</b>", reply_markup=markup)


async def chose_chats_for_delete(callback: CallbackQuery, _chosen, **kwargs):
    all_chats = db.select_data_db("rosennachev_welcome_bot", "chats")
    result = []

    for _ in all_chats:
        result.append({"id": _[0], "tittle": _[3], "chat_id": _[1]})

    markup = await delete_chats_check_keyboard(result, _chosen)
    await callback.message.edit_text(text="<b>🗑Моля, изберете чат за изтриване</b>",
                                     reply_markup=markup)


async def delete_chats_check(callback: CallbackQuery, _chosen, **kwargs):
    markup = await delete_chats_keyboard(_chosen)

    await callback.message.edit_text(text="<b>🗑Сигурен ли си, че искаш да изтриеш?</b>",
                                     reply_markup=markup)


async def delete_chat(callback: CallbackQuery, _chosen, _values, **kwargs):
    if _chosen == "yes":
        bad_request = ''
        try:
            await bot.leave_chat(_values)
        except ChatNotFound:
            bad_request = "\n" + str(ChatNotFound.text)
        db.delete_data_db("rosennachev_welcome_bot", "chats", f"chat_id = '{_values}'", "delete_records")
        logger.info(f"User: {callback.from_user.username}, Action: delete chat" + bad_request)

    await chose_chats_for_delete(callback, "delete_chats_check")


async def show_all_chats(callback: CallbackQuery, _chosen, _values, **kwargs):
    all_chats = db.select_data_db("rosennachev_welcome_bot", "chats")

    markup = await list_chats_keyboard()

    result = ""
    for _ in all_chats:
        text = f"<b>Чат {_[3]}\nДата на добавяне към чата {_[2]}\n\n</b>"
        result += text

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(text=f"<b>💬Списък на всички чатове\n\n{result}</b>", reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    chosen = callback_data.get("chosen")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    values = callback_data.get("values")

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "menu": list_menu,

        "chose_chats_for_delete": chose_chats_for_delete,  # Отдаем подкатегории
        "delete_chats_check": delete_chats_check,
        "delete_chat": delete_chat,

        "show_all_chats": show_all_chats,  # Отдаем товары

    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        _chosen=chosen,
        _values=values
    )


@dp.callback_query_handler(user_callback.filter())
async def callback_inline(query: types.CallbackQuery, callback_data: dict):
    being = callback_data.get("being")
    # айди пользователя (приходит строкой, поэтому используем int)
    user_id = int(callback_data.get("user_id"))
    # айди сообщения о присоединении
    user_join_message_id = int(callback_data.get("user_join_message_id"))
    # и айди чата, для последнующей выдачи прав
    chat_id = int(query.message.chat.id)

    # когда вытянул id проверь его тут и это будет функционал только для нового пользователя
    if query.from_user.id != user_id:
        await bot.answer_callback_query(
            query.id,
            text='Съобщение за друг потребител! (This message for another user!)',
            show_alert=True
        )
        return

    flags.update(flag=False)

    # далее, если пользователь выбрал кнопку "человек" сообщаем ему об этом
    if being == "human":
        logger.info(f"User: {query.from_user.id}, select human")
        text = str("Имате достъп до чата! You have access in our chat!")
        await bot.answer_callback_query(query.id,
                                        text=text,
                                        show_alert=True
                                        )
        try:
            await query.message.delete()
            welcome_message = user_join_message_id + 2
            await asyncio.sleep(5)
            await bot.delete_message(query.message.chat.id, welcome_message)
        except MessageToDeleteNotFound:
            logger.error("I get error: MessageToDeleteNotFound")

    # а если всё-таки бот, тоже отписываем и пропускаем, ибо только юзерботы могут жать на кнопки
    elif being == "bot":
        logger.info(f"User: {query.from_user.id}, select bot")
        text = str("Ти си бот! Отказан ви е достъп до чата! You are bot and access is closed in our chat!")

        await bot.answer_callback_query(
            query.id,
            text=text,
            show_alert=True
        )
        await asyncio.sleep(10)
        await query.message.chat.kick(user_id)

        try:
            await bot.delete_message(query.message.chat.id, user_join_message_id)
            await query.message.delete()
        except MessageToDeleteNotFound:
            logger.error("I get error: MessageToDeleteNotFound")

    # не забываем выдать юзеру необходимые права
    new_permissions = set_new_user_approved_permissions()
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=new_permissions,
    )
