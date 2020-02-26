from django.shortcuts import render

from core.forms import ConvertCurrencyForm
from core.serializers import CurrencyConverterSerializers
from currencyconverter.settings import CURRENCY_LIST, APP_ID

from rest_framework import viewsets, status
from rest_framework.response import Response
import requests


def home(request):
    context = {}
    if request.method == 'GET':
        currency_form = ConvertCurrencyForm()
        currency_form.set_currency_choices(CURRENCY_LIST)
        context['currency_form'] = currency_form
        return render(request, 'core/home.html', context)
    else:
        currency_form = ConvertCurrencyForm(request.POST)
        currency_form.set_currency_choices(CURRENCY_LIST)
        if currency_form.is_valid():
            data = currency_form.cleaned_data
            amount = convert(data.get('convert_from'), data.get('convert_into'), data.get('amount'))
            context['amount'] = amount

        context['currency_form'] = currency_form
        return render(request, 'core/home.html', context)


class ConvertCurrency(viewsets.ViewSet):
    def convert(self, request):
        serializer = CurrencyConverterSerializers(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            response = convert(data['convert_from'], data['convert_into'], data['amount'])
            return Response({"amount": response}, status=status.HTTP_200_OK)
        return Response({"Error": 'Invalid data'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


def convert(convert_from, convert_into, amount):
    convert_from = convert_from.upper()
    convert_into = convert_into.upper()
    if convert_from != convert_into:
        rates = get_rates()
        if convert_from and convert_into in rates:
            response = round(rates[convert_into] / rates[convert_from] * amount, 6)
            return response
    return 'Invalid data'


def get_rates():
    api_request = "https://openexchangerates.org/api/latest.json?app_id=" + APP_ID + "&symbols=" + ','.join(
        CURRENCY_LIST)
    api_request = requests.get(api_request)
    response_rates = api_request.json()['rates']
    return response_rates
