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

def get_list_coins():
    menu = [
        [InlineKeyboardButton(text="Bitcoin", callback_data='btc')], #,
        [InlineKeyboardButton(text="Ethereum", callback_data='eth')]
    ]

    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    print(menu)
    return menu

# coins_names = []
def get_all_coins():
    load_dotenv()
    engine = create_engine(os.getenv('DB_URL'))
    Session = sessionmaker(bind=engine)
    session = Session()
    coins_names_tuple = session.query(Coins_rates.coin_name).all()
    # print(coins_names_tuple) # request to data base gives us list of tuples with names of coins
    #creation of list of inline buttons
    coins_names_list = [x[0] for x in coins_names_tuple]

    # button_list = []
    # for name in coins_names_list:
    #     button = [InlineKeyboardButton(text=name[0], callback_data='coin')]
    #     button_list.append(button)
    # menu = InlineKeyboardMarkup(inline_keyboard=button_list)
    # pprint(menu)
    return coins_names_list



def get_coins_pages(page: int):
    """
     Функция для создания клавиатуры, три конопки в одном ряду ,  в спике не более 15 кнопок с названиями криптовалют
    """
    n = 15  # количество кнопок на странице
    coins = get_all_coins()
    quantity_of_pages = math.ceil(len(coins) / n)
    if page > quantity_of_pages:
        page = 1
    elif page < 1:
        page = quantity_of_pages
    coins_names = coins[(page-1)*n:page*n]
    print(coins_names)
    buttons = []



    # index = 0
    # while index < len(coins_names) - 2:
    #     # button = InlineKeyboardButton(text=name, callback_data=f'{name}_coin')
    #     for
    #     list_3_buttons_in_line = []
    #     first = coins_names[index]
    #     button1 = InlineKeyboardButton(text=f'{first}', callback_data=f'{first}_coin')
    #     second = coins_names[index + 1]
    #     button2 = InlineKeyboardButton(text=f'{second}', callback_data=f'{second}_coin')
    #     third = coins_names[index + 2]
    #     button3 = InlineKeyboardButton(text=f'{third}', callback_data=f'{third}_coin')
    #     list_3_buttons_in_line.extend([button1, button2, button3])
    #     buttons.append(list_3_buttons_in_line)
    #     index +=3

    # buttons.append([InlineKeyboardButton(text= '⬅️', callback_data=f'prev_{page}'),
    #      InlineKeyboardButton(text= '1'),
    #      InlineKeyboardButton(text= '➡️', callback_data=f'next_{page}')])
    #
    # menu = buttons


        # button = InlineKeyboardButton(text=name, callback_data=f'{name}_coin')
    # print(buttons)

    # menu = [
    #     [InlineKeyboardButton(text="Bitcoin", callback_data='Bitcoin_coin'),  # ,
    #     InlineKeyboardButton(text="Ethereum", callback_data='eth'),
    #     InlineKeyboardButton(text="Ton", callback_data='ton')],
    #
    #     [InlineKeyboardButton(text= '⬅️', callback_data=f'prev_{page}'),  # ,
    #      InlineKeyboardButton(text= '1'),
    #      InlineKeyboardButton(text= '➡️', callback_data=f'next_{page}')]
    #
    # ]


    # menu = InlineKeyboardMarkup(inline_keyboard=menu)
    # return menu

# get_coins_pages(1)

# print(menu)

# names = ['A', 'B', 'C',
#          'D', 'F', 'G',
#          'E', 'T', 'T']

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
    print(menu)
    return menu

# get_coins_pages(1)
#
# get_list_coins()