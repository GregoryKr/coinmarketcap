import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from dotenv import load_dotenv

from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.settings import text as txt
from bot.kb import get_menu, register_user, get_list_coins, get_coins_pages
from bot.settings.text import border_value_text
from bot.states import DataState
from bot.models import User, Coin, Base, Coins_rates
# from cmc.coinmarket import update_coin_table, url, coin_rate
from bot.comparison import compare


load_dotenv()

router = Router()

# update_coin_table(coin_rate=coin_rate, url=url)

# engine = create_engine(os.getenv('DB_URL'))
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

engine = create_async_engine(os.getenv('DB_URL'), echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Проверяет регистрацию пользователя, если пользователь зарегистрирован, направляет меню(клавиатуру).
    Если нет, то направляет меню для регистрации
    :param message:
    :return: None
    """
    user_id = message.from_user.id
    # session = Session()
    # user = session.query(User).filter_by(tg_id=user_id).first()
    # if user:
    #     await message.answer(text=txt.menu_text, reply_markup=get_menu())
    #     session.close()
    # else:
    #     await message.answer(text=txt.user_not_in_base, reply_markup=register_user())
    #     session.close()
    # Используем асинхронную сессию
    async with AsyncSessionLocal() as session:
        # Выполняем асинхронный запрос
        result = await session.execute(select(User).filter_by(tg_id=user_id))
        user = result.scalars().first()  # Получаем первый результат

        if user:
            await message.answer(text=txt.menu_text, reply_markup=get_menu())
        else:
            await message.answer(text=txt.user_not_in_base, reply_markup=register_user())


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
    Registration of user
    :param message: команда от пользователя
    :param state: объект состояния
    :return: None
    """
    name = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    if name.isalpha():
        async with AsyncSessionLocal() as session:  # Используем асинхронную сессию
            new_user = User(tg_id=user_id, name=name, chat_id=chat_id)  # Создаем объект пользователя
            session.add(new_user)  # Добавляем объект в сессию
            await session.commit()  # Асинхронно фиксируем изменения
        await message.answer(text=f'Welcome, {name}', reply_markup=get_menu())
    else:
        await state.set_state(DataState.name)
        await message.answer(text=txt.incorrect_name)


async def get_all_coins():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Coins_rates.coin_name))
        coins_names_tuple = result.scalars().all()  # Получаем все результ
    # coins_names_list = [x[0] for x in coins_names_tuple]
    print(coins_names_tuple)
    return coins_names_tuple

#
# @router.callback_query(F.data == "info")
# async def choose_coin(call: types.CallbackQuery) -> None:
#     """
#     Handler для выбора валюты
#     :param call:  call от пользователя
#     :param state: объект состояния
#     :return: None
#     """
#     # необходимо добавить функцию, которая покажет весь список монет
#     # await state.set_state(DataState.coin)
#     coins = await get_all_coins()
#     await call.message.answer(text=txt.choose_coin, reply_markup=get_coins_pages(page=1, coins=coins))


@router.callback_query(F.data == "info")
@router.callback_query(F.data.startswith("next"))
@router.callback_query(F.data.startswith("prev"))
async def change_page(call: types.CallbackQuery):
    """
    Handler для перелистывания страницы с коинами (прибавление страницы и уменьшение страницы)
    """
    coins = await get_all_coins()
    if call.data == "info":
        page = 1
    else:
        current_page = int(call.data.split('_')[1])
        if call.data.startswith("next"):
            page = current_page + 1
        else:
            page = current_page - 1

    await call.message.edit_reply_markup(reply_markup=get_coins_pages(page=page, coins=coins))


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
    async with AsyncSessionLocal() as session:
        # Выполняем асинхронный запрос
        # получаем текущую цену на валюту из бд
        result = await session.execute(select(Coins_rates).filter_by(coin_name=name_of_coin))
        coin = result.scalars().first()  # Получаем первый результат
    # with Session() as session:
    #     # получаем текущую цену на валюту из бд
    #     coin = session.query(Coins_rates).filter_by(coin_name=name_of_coin).first()
        price = round(coin.coin_price, 2)
    await call.message.answer(text=f"Текущая цена {name_of_coin}: {price} $")
    await state.update_data(name_of_coin=name_of_coin)

    await state.set_state(DataState.coin_btc)
    # await state.update_data(name_of_coin=name_of_coin)
    await call.message.answer(text=f'Введите граничное значение для {name_of_coin}')


@router.callback_query(F.data == "coins")
async def show_all_coins(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler для выведения в чат списка криптовалют пользователя
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    async with AsyncSessionLocal() as session:
        # Выполняем асинхронный запрос
        # получаем айди юзера из бд потом все монеты по айди юзера
        result = await session.execute(select(User).filter_by(tg_id=user_id))
        user = result.scalars().first()
        user_coins_id = user.id
        result = await session.execute(select(Coin).filter_by(user_id=user_coins_id))
        coins = result.scalars().all()  # Получаем все результаты
    my_coins = [] # список имен криптовалют пользователя
    for coin in coins:
        coin_name = coin.coin_name
        my_coins.append(coin_name)
        print(my_coins)
    text = "; ".join(my_coins) # получаем строку из списка с именами криптовалют пользователя
    await call.message.answer(text=text)


@router.message(DataState.coin_btc)
async def set_border_value_btc(message: Message, state: FSMContext) -> None:
    """
    Handler для установки граничного значения коина
    :param call:  call от пользователя
    :param state: объект состояния
    :return: None
    """
    coin_value = float(message.text)
    if coin_value >= 0:
        # with Session() as session:
        #     bitcoin = Coins_rates(coin_price=4, coin_name='Bitcoin')
        #     session.add(bitcoin)
        #     session.commit()
        coin_data = await state.get_data()
        # print(coin_data)
        name_of_coin = coin_data['name_of_coin']
        # print(name_of_coin)
        async with AsyncSessionLocal() as session:  # Используем асинхронную сессию
            user_id = message.from_user.id  # Получаем ID пользователя

            # Выполняем асинхронный запрос для получения пользователя
            user_result = await session.execute(select(User).filter_by(tg_id=user_id))
            user = user_result.scalars().first()  # Получаем первого пользователя

            # Выполняем асинхронный запрос для получения данных о валюте
            coin_result = await session.execute(select(Coins_rates).filter_by(coin_name=name_of_coin))
            coin = coin_result.scalars().first()  # Получаем данные о валюте
        # with Session() as session:
        #     user_id = message.from_user.id
        #     user = session.query(User).filter_by(tg_id=user_id).first()
        #     coin = session.query(Coins_rates).filter_by(coin_name=name_of_coin).first()
        #     print(coin)
            price = round(coin.coin_price, 2)
            # print(price)
            if coin_value < price:
                expectation = False
            elif coin_value > price:
                expectation = True
            else:
                await message.answer(text="Введите корректное значение граничной цены")
                await state.set_state(DataState.coin_btc)
            # Создаем объект Coin
            btc = Coin(
                coin_name=name_of_coin,
                border_value=float(coin_value),
                user_id=user.id,
                coin_id=coin.id,
                expectations=expectation
            )

            # Используем асинхронную сессию
            async with AsyncSessionLocal() as session:
                session.add(btc)  # Добавляем объект в сессию
                await session.commit()  # Асинхронно фиксируем изменения
            # btc = Coin(coin_name=name_of_coin, border_value=float(coin_value),
            #            user_id=user.id, coin_id=coin.id, expectations=expectation)
            # session.add(btc)
            # session.commit()
            # session.close()
        chat_id = message.chat.id
        # print(chat_id)
        # await compare(name_of_coin=name_of_coin, chat_id=chat_id)
        # print(result)
        await message.answer(text=txt.choose_coin, reply_markup=get_menu())
        # await compare(name_of_coin)
    else:
        await state.set_state(DataState.coin_btc)
        await message.answer(text="incorrect value")
    # необходимо добавить функцию, которая покажет весь список монет
    # await state.set_state(DataState.coin)




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
