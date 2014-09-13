from google.appengine.ext import ndb



from datetime import datetime


CACHE_TIMEOUT   =   12*3600

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
                data = func(self, endpoint, **kwargs)
                cr.data = data
                cr.put()

        return cr.data
    return cached_check



class CachedResponse(ndb.Model):
    endpoint = ndb.StringProperty('e', required=True, indexed=True)
    data = ndb.JsonProperty('d', required=True)
    timestamp = ndb.DateTimeProperty('t', auto_now=True)
