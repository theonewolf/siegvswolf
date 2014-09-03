from .util import US_URI, EN_US

PROFILE_ENDP    = 'profile/%s'
HERO_ENDP       = 'profile/%s/hero/%s'

class Hero:
    def __init__(self, stats):
        self.update(stats.items())

    def update(self, data):
        for k,v in data:
            if k == 'class': v = v.replace('-', ' ').title()
            setattr(self, k, v)

class D3:

    def __init__(self, uri=US_URI, locale=EN_US, api_key=None):
        self.bnet = BNetConnection(uri, locale, api_key)

    def get_profile(self, profile):
        return self.bnet.get(PROFILE_ENDP % profile)

    def get_hero(self, profile, hero):
        return Hero(self.bnet.get(HERO_ENDP % (profile, hero)))
