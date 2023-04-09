import time
import requests
from requests.exceptions import RequestException


def _exponential_backoff(retry):
    return 2 ** retry


class BaseApiRequest:
    def __init__(self, base_url, api_key=None, retries=1):
        self.base_url = base_url
        self.api_key = api_key
        self.retries = retries

    def get(self, endpoint, params):
        if self.api_key:
            params['apikey'] = self.api_key

        url = f'{self.base_url}{endpoint}'

        for attempt in range(self.retries + 1):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                if attempt == self.retries:
                    raise e
                else:
                    wait_time = _exponential_backoff(attempt)
                    time.sleep(wait_time)
