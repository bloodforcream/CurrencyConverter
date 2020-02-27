import requests

from currencyconverter.settings import CURRENCY_LIST, APP_ID


def convert(convert_from, convert_into, amount):
    convert_from = convert_from.upper()
    convert_into = convert_into.upper()
    rates = get_rates()
    if convert_from in rates and convert_into in rates:
        response = round(rates[convert_into] / rates[convert_from] * amount, 6)
        return response
    else:
        return 'Unsupported currency'


def get_rates():
    api_request = "https://openexchangerates.org/api/latest.json?app_id=" + APP_ID + "&symbols=" + ','.join(
        CURRENCY_LIST)
    api_request = requests.get(api_request)
    response_rates = api_request.json()['rates']
    return response_rates
