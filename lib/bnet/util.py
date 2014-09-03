import requests

URI_US = 'https://us.api.battle.net/d3/'
EN_US  = 'en_US'

def cached(func):
    @wraps(func)
    def cached_check(endpoint, **kwargs):
        return func(endpoint, **kwargs)
    return cached_check


class BNetConnection:
    
    def __init__(self, uri=US_URI, locale=EN_US, api_key=None):
        self.api_key = api_key
        self.locale = locale
        self.uri = uri

    @cached
    def get(endpoint, **kwargs):
        kwargs['locale'] = self.locale
        kwargs['apikey'] = self.api_key

        r = requests.get(self.uri + endpoint, params=kwargs).json()
