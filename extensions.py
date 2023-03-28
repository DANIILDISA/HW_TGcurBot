import json
import requests
from config import keys

class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str) -> float:
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        response_json = json.loads(response.text)

        if base_ticker not in response_json:
            raise ConvertionException(f'Не удалось получить курс {base_ticker} к {quote_ticker}.')

        exchange_rate = response_json[base_ticker]

        total_base = exchange_rate * amount
        return total_base