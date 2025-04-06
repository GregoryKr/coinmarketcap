import os
import asyncio

from sqlalchemy import create_engine, result_tuple, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from aiogram.methods.send_message import SendMessage
from sqlalchemy.testing.suite.test_reflection import users

# from bot.handlers import engine, Session
from cmc.coinmarket import session
from bot.models import User, Coin, Coins_rates
# import main
# from bot.handlers import name_of_coin
import time

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

#
# while True:
#     time.sleep(7)
# name_of_coin в функцию не передавать
async def compare() -> None:
    """
    Функция для сравнения граничного значения и текущей цены токена
    пройти циклом по все заявкам из coins где есть инфа и запустить
    функцию сравнения (по индексу обращаемся к граничной цене и сравниваем)
    """
    while True:
        # if coins:
        engine = create_async_engine(os.getenv('DB_URL'), echo=False)
        AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        # engine = create_engine(os.getenv('DB_URL'))
        # Session = sessionmaker(bind=engine)
        async with AsyncSessionLocal() as session:
            # coin_info = await session.query(Coin).all()
            coin_info_result = await session.execute(select(Coin))
            coin_info = coin_info_result.scalars().all()
            # coin = session.query(Coins_rates).all()
            # users = session.query(User).all()
            # for user in users:
            #     chat_id = user.chat_id
            #     id = user.id
            for coin in coin_info:
                coin_name = coin.coin_name
                user_id = coin.user_id
                id_ = coin.id # coin id in Coin
                # if user_id == id:
                coin_object_result = await session.execute(
                    select(Coins_rates).filter_by(coin_name=coin_name)
                )
                coin_object = coin_object_result.scalars().first()
                coin_current_price = round(coin_object.coin_price, 2)
                border_value = coin.border_value
                # достать чат айди
                expect = coin.expectations
                text = (f'{coin_name}\n текущая цена: {coin_current_price}\n '
                        f'граничное значение: {border_value} ')
                stmt = select(User).filter_by(id=user_id)  # Создаём запрос
                result = await session.execute(stmt)  # Выполняем запрос
                user = result.scalars().first()  # Получаем первый результат или None
                chat_id = user.chat_id
                # удалить запись в Coins, как условие выполнилось
                if coin_current_price >= border_value and expect is True:
                    await bot.send_message(chat_id, text)
                    stmt = delete(Coin).where(Coin.id == id_)
                    await session.execute(stmt)
                    await session.commit()  # Подтверждаем удаление

                elif coin_current_price <= border_value and expect is False:
                    await bot.send_message(chat_id, text)
                    stmt = delete(Coin).where(Coin.id == id_)
                    await session.execute(stmt)
                    await session.commit()  # Подтверждаем удаление

        # print('okay')
        await asyncio.sleep(3)

# await compare()
    # engine = create_engine(os.getenv('DB_URL'))
    # Session = sessionmaker(bind=engine)
    # with Session() as session:
    #     # получаем текущую цену на валюту из бд
    #     coin = session.query(Coins_rates).filter_by(coin_name=name_of_coin).first()
    #     price = coin.coin_price
    #     print(price)
    #     # получаем граничную цену из бд
    #     coin_marketcap = session.query(Coin).filter_by(coin_name=name_of_coin).first()
    #     border_price = coin_marketcap.border_value
    #     expect = coin_marketcap.expectations
    #     print(border_price)
    #     # while True:
        # time.sleep(11)
        # expect = session.query(Coin).filter_by(coin_name=name_of_coin).first()
        # border_price = coin_marketcap.border_value
        # if expect and border_price >= price:
        #     print(f"price:{price}, lets sell")
        # elif not expect and border_price <= price:
        #     print(f"price: {price}, lets buy")

        # await bot.send_message(chat_id, 'ok')





