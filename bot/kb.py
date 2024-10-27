from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu():
    menu = [
        [InlineKeyboardButton(text="Выбрать криптовалюту", callback_data="info")]#,
        # [InlineKeyboardButton(text="История тренировок", callback_data="history")]
    ]

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu


def register_user():
    menu = [
        [InlineKeyboardButton(text="Начать ввод данных", callback_data="data")]
    ]

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu



