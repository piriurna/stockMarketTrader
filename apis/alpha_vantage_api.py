import pandas as pd
from .base_api_request import BaseApiRequest

BASE_URL = 'https://www.alphavantage.co/query'
API_FUNCTION = 'TIME_SERIES_DAILY_ADJUSTED'
OUTPUT_SIZE = 'full'


def _process_stock_data(stock_data):
    df = pd.DataFrame.from_dict(stock_data, orient='index')
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    # Convert string columns to numeric data types
    numeric_columns = ['1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume',
                       '7. dividend amount', '8. split coefficient']
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    return df


class AlphaVantageApi(BaseApiRequest):
    def __init__(self, api_key):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def fetch_stock_data(self, symbol):
        params = {
            'function': API_FUNCTION,
            'symbol': symbol,
            'outputsize': OUTPUT_SIZE,
        }
        json_data = self.get('', params)
        stock_data = json_data['Time Series (Daily)']
        return _process_stock_data(stock_data)
