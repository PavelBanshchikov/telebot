import requests
import json
from config import keys


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote, base, amount):
        if quote == base:
            raise APIException('Невозможно перевести одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        if not amount.isdigit():
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        dict_data = json.loads(r.content)[keys[base]]
        total_base = float(dict_data) * float(amount)
        return total_base