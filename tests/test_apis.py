import unittest
from unittest.mock import patch
from apis import BaseApiRequest
from apis import AlphaVantageApi


class TestBaseApiRequest(unittest.TestCase):
    def setUp(self):
        self.base_api_request = BaseApiRequest('https://api.example.com')

    @patch('apis.base_api_request.requests.get')
    def test_get(self, mock_get):
        self.base_api_request.get('/test', {})
        mock_get.assert_called_once_with('https://api.example.com/test', params={})


class TestAlphaVantageApi(unittest.TestCase):
    def setUp(self):
        self.alpha_vantage_api = AlphaVantageApi('test_api_key')

    @patch('apis.base_api_request.requests.get')
    def test_fetch_stock_data(self, mock_get):
        self.alpha_vantage_api.fetch_stock_data('MSFT')
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': 'MSFT',
            'outputsize': 'full',
            'apikey': 'test_api_key',
        }
        mock_get.assert_called_once_with('https://www.alphavantage.co/query', params=params)


if __name__ == '__main__':
    unittest.main()
