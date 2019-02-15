"""
Created: 2/15/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from threading import Thread


def thread(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def cache_app(f):
    global _result
    _result = None

    def wrapper(*args, **kwargs):
        if 'force_new' in kwargs.keys():
            if kwargs['force_new']:
                del kwargs['force_new']
                return f(*args, **kwargs)

            del kwargs['force_new']

        global _result

        if _result is None:
            _result = f(*args, **kwargs)
        return _result

    return wrapper