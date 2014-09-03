from .util import URI_US, EN_US, BNetConnection

PROFILE_ENDP    = 'profile/%s/'
HERO_ENDP       = PROFILE_ENDP + 'hero/%s'
GENDER          = { 0 : 'Male', 1 : 'Female' }

class Hero:
    def __init__(self, stats):
        self.update(stats.items())

    def update(self, data):
        for k,v in data:
            if k == 'class': v = v.replace('-', ' ').title()
            if k == 'gender': v = GENDER[v]
            setattr(self, k, v)

class Season:
    def __init__(self, stats):
        self.update(stats.items())

    def update(self, data):
        for k,v in data:
            setattr(self, k, v)

class Profile:
    def __init__(self, stats):
        self.update(stats.items())

    def update(self, data):
        for k,v in data:
            setattr(self, k, v)


class D3:

    def __init__(self, uri=URI_US, locale=EN_US, api_key=None):
        self.bnet = BNetConnection(uri, locale, api_key)

    def get_profile(self, profile):
        return Profile(self.bnet.get(PROFILE_ENDP % profile))

    def get_hero(self, profile, hero):
        return Hero(self.bnet.get(HERO_ENDP % (profile, hero)))
