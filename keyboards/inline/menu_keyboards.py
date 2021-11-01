from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import deep_linking
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "chosen", "values")
# создём CallbackData для удобного парсинга калбеков
user_callback = CallbackData("confirm", "being", "user_id", "user_join_message_id")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, chosen="0", values="0"):
    return menu_cd.new(level=level, chosen=chosen, values=values)


def generate_confirm_markup(user_id: int, user_join_message_id: int) -> InlineKeyboardMarkup:
    """
    Функция, создающая клавиатуру для подтверждения, что пользователь не является ботом
    """

    # создаём инлайн клавиатуру
    confirm_user_markup = InlineKeyboardMarkup(row_width=2)

    # и добавляем в неё 2 кнопки
    confirm_user_markup.add(
        # кнопка "человек", в калбеке которой будет лежать confirm:human:<user_id>
        InlineKeyboardButton(
            "Я человек",
            callback_data=user_callback.new(
                being="human",
                user_id=user_id,
                user_join_message_id=user_join_message_id
            )
        ),
        # и кнопка "bot", в калбеке которой будет лежать confirm:bot:<user_id>
        InlineKeyboardButton(
            "Я бот",
            callback_data=user_callback.new(
                being="bot",
                user_id=user_id,
                user_join_message_id=user_join_message_id
            )
        ),
    )

    # отдаём клавиатуру после создания
    return confirm_user_markup


# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def menu_keyboard():
    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=3, column_width=2)

    # Сформируем текст, который будет на кнопке
    button_text = ["💭Добавить чат", "🗯Удалить чат", "💬Все чаты"]

    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    callback_data_del = make_callback_data(level="chose_chats_for_delete", chosen="delete_chats_check")
    callback_data_show_all = make_callback_data(level="show_all_chats")

    # Вставляем кнопку в клавиатуру
    markup.add(
        InlineKeyboardButton(text=button_text[0], url=await deep_linking.get_startgroup_link('test')),
        InlineKeyboardButton(text=button_text[1], callback_data=callback_data_del),
        InlineKeyboardButton(text=button_text[2], callback_data=callback_data_show_all),
    )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


async def delete_chats_check_keyboard(chats, _chosen):
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup(row_width=2)

    # Сформируем текст, который будет на кнопке
    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    for chat in chats:
        callback_data_del = make_callback_data(level=_chosen, chosen=str(chat.get('chat_id')))

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=chat.get('tittle'), callback_data=callback_data_del)
        )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="menu")
        )
    )
    return markup


async def delete_chats_keyboard(_id):
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup()

    # Сформируем текст, который будет на кнопке
    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    markup.row(
        InlineKeyboardButton(
            text="✅УДАЛИТЬ",
            callback_data=make_callback_data(level="delete_chat", chosen="yes", values=_id)
        )
    )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="delete_chat", chosen="no")
        )
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
async def list_chats_keyboard():
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup()

    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="menu")
        )
    )
    return markup