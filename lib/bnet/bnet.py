from .cache import cached
from .util import raw_get

URI_US = 'https://us.api.battle.net/d3/'
EN_US  = 'en_US'

class BNetConnection:
    
    def __init__(self, uri=URI_US, locale=EN_US, api_key=None):
        self.api_key = api_key
        self.locale = locale
        self.uri = uri

    @cached(600)
    def get(self, endpoint, **kwargs):
        return raw_get(self, endpoint, **kwargs)
