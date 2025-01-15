import os
import time

from sqlalchemy import create_engine, result_tuple
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean

# from bot.handlers import engine, Session
from cmc.coinmarket import session
from bot.models import User, Coin, Coins_rates
import time

#
# while True:
#     time.sleep(7)
def compare() -> Boolean:
    """
    Функция для сравнения граничного значения и текущей цены токена
    """
    engine = create_engine(os.getenv('DB_URL'))
    Session = sessionmaker(bind=engine)
    with Session() as session:
        # получаем текущую цену на валюту из бд
        coin = session.query(Coins_rates).filter_by(coin_name='Bitcoin').first()
        price = coin.coin_price
        print(price)
        # получаем граничную цену из бд
        coin_marketcap = session.query(Coin).filter_by(coin_name='Bitcoin').first()
        border_price = coin_marketcap.border_value
        print(border_price)
        if price <= border_price:
            return True
        else:
            return False


result = compare()
print(result)