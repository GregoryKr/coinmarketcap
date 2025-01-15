import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.settings import text as txt
from bot.kb import get_menu, register_user, get_list_coins, get_coins_pages, get_all_coins
from bot.settings.text import border_value_text
from bot.states import DataState
from bot.models import User, Coin, Base, Coins_rates
# from cmc.coinmarket import update_coin_table, url, coin_rate
from bot.comparison import compare, result


load_dotenv()

router = Router()

# update_coin_table(coin_rate=coin_rate, url=url)

engine = create_engine(os.getenv('DB_URL'))
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Проверяет регистрацию пользователя, если пользователь зарегистрирован, направляет меню(клавиатуру).
    Если нет, то направляет меню для регистрации
    :param message:
    :return: None
    """
    user_id = message.from_user.id
    session = Session()
    user = session.query(User).filter_by(tg_id=user_id).first()
    if user:
        await message.answer(text=txt.menu_text, reply_markup=get_menu())
        session.close()
    else:
        await message.answer(text=txt.user_not_in_base, reply_markup=register_user())
        session.close()


@router.callback_query(F.data == "data")
async def registration_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler для запуска процесса регистрации
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    await state.set_state(DataState.name)
    await call.message.answer(text=txt.name)

@router.message(DataState.name)
async def name_handler(message: Message, state: FSMContext) -> None:
    """
    Проверяет корректность ввода возраста и устанавливает DataState.height
    :param message: команда от пользователя
    :param state: объект состояния
    :return: None
    """
    name = message.text
    user_id = message.from_user.id
    if name.isalpha():
        with Session() as session:
            new_user = User(tg_id=user_id, name=name)
            session.add(new_user)
            session.commit()
    # await state.set_state(DataState.coin)
        await message.answer(text=f'Welcome, {name}', reply_markup=get_menu())
    else:
        await state.set_state(DataState.name)
        await message.answer(text=txt.incorrect_name)

@router.callback_query(F.data == "info")
async def choose_coin(call: types.CallbackQuery) -> None:
    """
    Handler для выбора валюты
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    # необходимо добавить функцию, которая покажет весь список монет
    # await state.set_state(DataState.coin)
    await call.message.answer(text=txt.choose_coin, reply_markup=get_coins_pages(page=1))

@router.callback_query(F.data.startswith("next"))
@router.callback_query(F.data.startswith("prev"))
async def change_page(call: types.CallbackQuery):
    """
    Handler для перелистывания страницы с коинами (прибавление страницы и уменьшение страницы)
    """
    current_page = int(call.data.split('_')[1])
    if call.data.startswith("next"):
        page = current_page + 1
    else:
        page = current_page - 1
    await call.message.edit_reply_markup(reply_markup=get_coins_pages(page))


@router.callback_query(F.data.endswith("coin"))
async def enter_border_value_btc(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler для установки состояния для ввода граничного значения
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    name_of_coin = call.data.split('_')[0]
    print(name_of_coin)
    await state.update_data(name_of_coin=name_of_coin)

    await state.set_state(DataState.coin_btc)
    # await state.update_data(name_of_coin=name_of_coin)
    await call.message.answer(text=f'Введите граничное значение для {name_of_coin}')


@router.message(DataState.coin_btc)
async def set_border_value_btc(message: Message, state: FSMContext) -> None:
    """
    Handler для установки граничного значения коина
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    coin_value = message.text
    if int(coin_value) >= 0:
        # with Session() as session:
        #     bitcoin = Coins_rates(coin_price=4, coin_name='Bitcoin')
        #     session.add(bitcoin)
        #     session.commit()
        coin_data = await state.get_data()
        print(coin_data)
        name_of_coin = coin_data['name_of_coin']
        print(name_of_coin)
        with Session() as session:
            user_id = message.from_user.id
            user = session.query(User).filter_by(tg_id=user_id).first()
            coin = session.query(Coins_rates).filter_by(coin_name=name_of_coin).first()
            print(coin)
            price = coin.coin_price
            print(price)
            btc = Coin(coin_name=name_of_coin, border_value=int(coin_value), user_id=user.id, coin_id=coin.id)
            session.add(btc)
            session.commit()
            session.close()

            await message.answer(text=txt.choose_coin, reply_markup=get_list_coins())
            # await state.set_state(DataState.border_value)
    else:
        await state.set_state(DataState.coin_btc)
        await message.answer(text="incorrect value")
    # необходимо добавить функцию, которая покажет весь список монет
    # await state.set_state(DataState.coin)

@router.message(DataState.border_value)
async def comparison_border_value_and_price(message: Message, state: FSMContext) -> None:
    """
    Функция для отправки сообщения, если цена коина ниже граничной цены
    return: None
    """
    if result:
        await message.answer(text=txt.border_value_text)
    else:
        await state.set_state(DataState.border_value)



@router.callback_query(F.data == "eth")
async def enter_border_value_eth(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler для установки граничного значения eth
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    await state.set_state(DataState.coin_eth)
    await call.message.answer(text='enter border value for Ethereum')

@router.message(DataState.coin_eth)
async def set_border_value_eth(message: Message, state: FSMContext) -> None:
    """
    Handler для установки граничного значения eth
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    eth_value = message.text
    if int(eth_value) >= 0:
        await message.answer(text=txt.choose_coin, reply_markup=get_list_coins())
    else:
        await state.set_state(DataState.coin_eth)
        await message.answer(text="incorrect value")
    # необходимо добавить функцию, которая покажет весь список монет
    # await state.set_state(DataState.coin)


# @router.message(DataState.coin)
# async def border_value(message: Message, state: FSMContext) -> None:
#     """
#     Добавляет введенные границы в базу данных
#     :param message: команда от пользователя
#     :param state: объект состояния
#     :return: None
#     """
#     border_value = message.text
    # try:
    #     border_value = float(border_value)
    #     await state.set_state(DataState.border_value)
    #     await message.answer(text=f"Выбрана валюта {border_value} USD")
    # except ValueError:
    #     await state.set_state(DataState.coin)
    #     await message.answer(text=txt.incorrect_border_value)
