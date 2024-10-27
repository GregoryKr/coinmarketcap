from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()


# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
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
parameters = {
  'listing_status': 'active'
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  # pprint(data['data'][0]['name'])
  coins_list = []
  for coin in data['data']:
    coins_list.append(coin['name'])
  pprint(coins_list)
  print(type(data))
  # pprint(data['data'][0]['name'])
  # for j in data:
  #   pprint(j[4])
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)