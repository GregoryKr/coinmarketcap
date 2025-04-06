from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
from dotenv import load_dotenv
from bot.models import Base, Coins_rates as coin_rate
import os
import psycopg2
import time


print(coin_rate)
load_dotenv()


# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest'
# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# parameters = {
#   'start':'1',
#   'limit':'5000',
#   'convert':'USD'
# }
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.getenv("TOKEN_CMC"),
}
# parameters = {
#   'id': 1
# }
# parameters = {
#   'listing_status': 'active'
# }

session = Session()
session.headers.update(headers)

try:
  """
  Отправляем запрос к базе данных
  """
  response = session.get(url) #, params=parameters отправляем запрос к  API CMC
  data = json.loads(response.text)
  # pprint(data)
  # pprint(data['data'][0]['name'])


  coins_list = []
  for coin in data['data']:
    coins_list.append((coin['name'], coin['quote']['USD']['price']))
  # pprint(coins_list)
  #
  # print(type(data))
  # pprint(data['data'][0]['name'])
  # for j in data:
  #   pprint(j[4])
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

conn = psycopg2.connect(dbname="coin_bot", user="postgres", password="03121981", host="127.0.0.1")
cursor = conn.cursor()
# cursor.execute("TRUNCATE coin_rate CASCADE")
# cursor.execute('ALTER SEQUENCE coin_rate_id_seq RESTART WITH 1;')
# cursor.executemany("INSERT INTO coin_rate(coin_name, coin_price) VALUES (%s, %s)", coins_list)

conn.commit()

# print("Данные добавлены")

def update_coin_table():
  """
  Функция для обновления данных (цены) в таблице coin_rate
  """
  try:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    conn = psycopg2.connect(dbname="coin_bot", user="postgres", password="03121981", host="127.0.0.1")
    cursor = conn.cursor()
    while True:
      time.sleep(10)
      response = session.get(url)  # , params=parameters
      data = json.loads(response.text)
      coins_list_updated = []
      for coin in data['data']:
        coins_list_updated.append((coin['name'], coin['quote']['USD']['price']))
      # pprint(coins_list_updated)
      # print("обновленный список")

      # cursor.execute('ALTER SEQUENCE table_id_seq RESTART WITH 1;')
      cursor.executemany("UPDATE coin_rate SET coin_price=%s WHERE coin_name=%s", ([(price, name) for name, price in coins_list_updated]))
      # cursor.executemany("UPDATE coin_rate SET coin_name=%s, coin_price=%s FROM (VALUES(coins_list_updated))")

      conn.commit()

      print('Данные обновлены')
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

# update_coin_table()
