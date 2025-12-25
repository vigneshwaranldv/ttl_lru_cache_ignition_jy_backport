from collections import OrderedDict
import threading, time

def ttl_lru_cache(maxsize=128, ttl=3600):
    """
    LRU cache backport for use in Ignition Jython/python 2.7 version
    
    :param maxsize: maximum unique func-param cache of 128
    :param ttl: default time-to-live - 3600 seconds/1 hour
    """

    def decorating_function(user_function):
        cache = OrderedDict()
        lock = threading.RLock()

        def wrapper(*args, **kwargs):
            key = args
            if kwargs:
                key += tuple(sorted(kwargs.items()))
            
            now = time.time()
            with lock:
                # purge stale entries
                keys_to_delete = [k for k,(ts,_) in cache.items() if now - ts >= ttl]
                for k in keys_to_delete:
                    del cache[k]
                # hit?
                if key in cache:
                    ts, val = cache.pop(key)
                    cache[key] = (ts, val)
                    return val
                
                #miss -> compute
                result = user_function(*args, **kwargs)
                with lock:
                    cache[key] = (now, result)
                    if len(cache) > maxsize:
                        cache.popitem(last=False)
                return result
            
            wrapper.cache_clear = lambda: cache.clear()
            wrapper.cache_info = lambda:{
                'hits':None,
                'misses':None,
                'current':len(cache),
                'maxsize':maxsize,
                'ttl':ttl
            }    

        return wrapper

    return decorating_function
