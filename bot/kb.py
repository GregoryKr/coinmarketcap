import os
import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from bot.handlers import engine
from bot.models import Coins_rates
# from cmc.coinmarket import coins_list
from pprint import pprint
# from bot.states import DataState


def get_menu():
    menu = [
        [InlineKeyboardButton(text="Выбрать криптовалюту", callback_data="info")],
        [InlineKeyboardButton(text="Мои криптовалюты", callback_data="coins")]
    ]

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu


def register_user():
    menu = [
        [InlineKeyboardButton(text="Начать ввод данных", callback_data="data")]
    ]

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu

def get_list_coins():
    menu = [
        [InlineKeyboardButton(text="Bitcoin", callback_data='btc')], #,
        [InlineKeyboardButton(text="Ethereum", callback_data='eth')]
    ]

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    # print(menu)
    return menu

# coins_names = []
# def get_all_coins():
#     load_dotenv()
#     engine = create_engine(os.getenv('DB_URL'))
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     coins_names_tuple = session.query(Coins_rates.coin_name).all()
#     coins_names_list = [x[0] for x in coins_names_tuple]
#
#     return coins_names_list



def get_coins_pages(page: int, coins: list):
    """
     Функция для создания клавиатуры, три конопки в одном ряду ,  в спике не более 15 кнопок с названиями криптовалют
    """
    n = 15  # количество кнопок на странице
    # coins = get_all_coins()
    quantity_of_pages = math.ceil(len(coins) / n)
    if page > quantity_of_pages:
        page = 1
    elif page < 1:
        page = quantity_of_pages
    coins_names = coins[(page-1)*n:page*n]
    print(coins_names)
    buttons = []

    step = 3
    for i in range(math.ceil(len(coins_names)/step)):
        crypto_names = coins_names[i*step:(i+1)*step]
        for index, crypto_name in enumerate(crypto_names):
            button_new = InlineKeyboardButton(text=f"{crypto_name}", callback_data=f'{crypto_name}_coin')
            crypto_names[index] = button_new
        buttons.append(crypto_names)
    # quantity_of_pages = math.ceil(len(coins)/n)

    buttons.append([InlineKeyboardButton(text= '⬅️', callback_data=f'prev_{page}'),
         InlineKeyboardButton(text= f'{page}/{quantity_of_pages}', callback_data='w'),
         InlineKeyboardButton(text= '➡️', callback_data=f'next_{page}')])

    menu = buttons
    # print(menu)

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    # print(menu)
    return menu

# get_coins_pages(1)
#
# get_list_coins()