from django.test import TestCase, Client
from django.urls import reverse

from unittest.mock import patch
from rest_framework.test import APITestCase


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_home_POST(self):
        with patch('core.views.convert') as mocked_convert:
            mocked_convert.return_value = 20
            response = self.client.post(self.home_url, data={
                'convert_from': 'USD',
                'convert_into': 'EUR',
                'amount': '10',
            })

            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'core/home.html')
            self.assertEquals(response.context['amount'], 20)


class ConverterTestCase(TestCase):
    def test_convert(self):
        with patch('core.converter.get_rates') as mocked_get_rates:
            mocked_get_rates.return_value = {'CZK': 23.232026, 'EUR': 0.919583, 'PLN': 3.95897, 'USD': 1}
            response = self.client.post(reverse('home'), data={
                'convert_from': 'USD',
                'convert_into': 'EUR',
                'amount': '1',
            })
            self.assertEquals(response.context['amount'], 0.919583)


class ApiTestCase(APITestCase):
    def setUp(self):
        self.api_convert_url = reverse('api-convert')

    def test_api_convert(self):
        with patch('core.converter.get_rates') as mocked_get_rates:
            mocked_get_rates.return_value = {'CZK': 23.232026, 'EUR': 0.919583, 'PLN': 3.95897, 'USD': 1}
            data = {'convert_from': 'USD', 'convert_into': 'EUR', 'amount': '1'}
            response = self.client.get(self.api_convert_url, data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['amount'], 0.919583)

    def test_api_convert_invalid_data(self):
        data = {'convert_from': 'USD', 'convert_into': 'EUR', 'amount': 'oops'}
        response = self.client.get(self.api_convert_url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Invalid data')

    def test_api_convert_unsupported_currency(self):
        data = {'convert_from': 'UDD', 'convert_into': 'RUB', 'amount': '1'}
        response = self.client.get(self.api_convert_url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['Error'], 'Unsupported currency')
