from django.shortcuts import render

from core.forms import ConvertCurrencyForm
from core.serializers import CurrencyConverterSerializers
from currencyconverter.settings import CURRENCY_LIST
from core.converter import convert
from rest_framework import viewsets, status
from rest_framework.response import Response


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
            if response != 'Unsupported currency':
                return Response({"amount": response}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": response}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
