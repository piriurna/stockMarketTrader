import requests


class BaseApiRequest:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params):
        if self.api_key:
            params['apikey'] = self.api_key

        url = f'{self.base_url}{endpoint}'
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
