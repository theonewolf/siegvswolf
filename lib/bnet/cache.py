import logging
from .util import raw_get



from google.appengine.api.taskqueue import TaskAlreadyExistsError
from google.appengine.api.taskqueue import TombstonedTaskError
from google.appengine.ext import ndb
from google.appengine.ext import deferred



from datetime import datetime
from time import time


CACHE_TIMEOUT   =  30

def update_cache(self, endpoint, **kwargs):
    data = raw_get(self, endpoint, **kwargs)
    key = ndb.Key(CachedResponse, endpoint)
    cr = key.get()
    cr.data = data
    cr.put()

def cached(timeout=CACHE_TIMEOUT):
    def func_wrapper(func):
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
                oldtime = cr.timestamp
                ts = time()
                currtime = datetime.utcfromtimestamp(ts)

                td = currtime - oldtime

                if td.seconds > timeout:
                    try:
                        task_name = endpoint.replace('/', '-') + \
                                    '-%d' % (int(ts))
                        deferred.defer(update_cache, self, endpoint,
                                       _name=task_name, **kwargs)
                    except TaskAlreadyExistsError:
                        logging.critical('Task <%s> already exists.' %
                                         task_name)
                        logging.critical('Could not update cache.')
                    except TombstonedTaskError:
                        logging.critical('Tombstoned task <%s> encountered.' %
                                         task_name)
                        logging.critical('Attempting to serve old cache data.')
                        logging.critical('Stored timestamp was: %s' %
                                         str(cr.timestamp))
                        logging.critical('Current time is: %s' % str(currtime))

            return cr.data
        return cached_check
    return func_wrapper 



class CachedResponse(ndb.Model):
    endpoint = ndb.StringProperty('e', required=True, indexed=True)
    data = ndb.JsonProperty('d', required=True)
    timestamp = ndb.DateTimeProperty('t', auto_now=True)
