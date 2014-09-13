from .util import raw_get



from google.appengine.ext import ndb
from google.appengine.ext import deferred



from datetime import datetime


CACHE_TIMEOUT   =  30

def update_cache(self, endpoint, **kwargs):
    data = self.get(endpoint, **kwargs)
    key = ndb.Key(CachedResponse, endpoint)
    cr = key.get()
    cr.data = data
    cr.put()

def cached(func):
    def cached_check(self, endpoint, **kwargs):
        key = ndb.Key(CachedResponse, endpoint)
        cr = key.get()
        if not cr:
            data = func(self, endpoint, **kwargs)
            cr = CachedResponse(key=key,
                                endpoint=endpoint,
                                data=data)
            cr.put()
        else:
            ts = cr.timestamp
            currtime = datetime.utcnow()

            td = currtime - ts

            if td.seconds > CACHE_TIMEOUT:
                deferred.defer(update_cache, self, endpoint,
                               _name=endpoint.replace('/', '-'), **kwargs)

        return cr.data
    return cached_check



class CachedResponse(ndb.Model):
    endpoint = ndb.StringProperty('e', required=True, indexed=True)
    data = ndb.JsonProperty('d', required=True)
    timestamp = ndb.DateTimeProperty('t', auto_now=True)
