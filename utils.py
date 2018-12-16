from timeit import default_timer
import requests


def profile(func):
    def wrapper(*args, **kwargs):
        start = default_timer()
        res = func(*args, **kwargs)
        end = default_timer()
        print("Execution time: ", format(end - start), " Result: ", res)
        return res

    return wrapper


class timer:
    def __enter__(self):
        self._start = default_timer()
        return self

    def __exit__(self, type, value, traceback):
        print("Execution time", format(default_timer() - self._start))
        return self


class SafeRequest(object):
    def __init__(self, timeout=3, default=None):
        self._timeout = timeout
        self._default = default

    def __call__(self, method, url, headers):
        try:
            return requests.request(method=method, url=url, headers=headers, timeout=self._timeout)
        except requests.exceptions.HTTPError as e:
            if self._default:
                return self._default
            else:
                raise e
        except requests.exceptions.RequestException as e:
            raise e
