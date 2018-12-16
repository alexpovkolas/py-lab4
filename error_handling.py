import logging
import time


def handle_error(exc_type=Exception, tries=1, delay=0, backoff=1, re_raise=True, log_traceback=True):
    params = {'tries': tries, 'delay': delay}

    def decorator(func):
        def inner(*args, **kwargs):
            while params['tries'] is None or params['tries']:
                try:
                    return func(*args, **kwargs)
                except exc_type as e:
                    params['retries'] -= 1
                    if log_traceback:
                        logging.error('Error', e)

                    time.sleep(params['current_delay'])
                    params['current_delay'] *= backoff
                    if re_raise:
                        raise
        return inner
    return decorator


class handle_error_context(object):
    def __init__(self, exc_type=Exception, tries=1, delay=0, backoff=1, re_raise=True, log_traceback=True):
        self._exc_type = exc_type
        self._tries = tries
        self._delay = delay
        self._backoff = backoff
        self._re_raise = re_raise
        self._log_traceback = log_traceback

    def __enter__(self):
        return self

    def __exit__(self, typ, val, traceback):
        pass

    def __call__(self, f):
        decorator = handle_error(self._exc_type, self._tries, self._delay, self._backoff, self._re_raise, self._log_traceback)
        return decorator(f)

