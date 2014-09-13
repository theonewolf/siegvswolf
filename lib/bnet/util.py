from cache import cached

import requests

URI_US = 'https://us.api.battle.net/d3/'
EN_US  = 'en_US'

class BNetConnection:
    
    def __init__(self, uri=URI_US, locale=EN_US, api_key=None):
        self.api_key = api_key
        self.locale = locale
        self.uri = uri

    @cached
    def get(self, endpoint, **kwargs):
        kwargs['locale'] = self.locale
        kwargs['apikey'] = self.api_key

        r = requests.get(self.uri + endpoint, params=kwargs)
        return r.json()
