import time
import os

from colored_print import ColoredPrint

log = ColoredPrint()

__author__ = "aGn"
__copyright__ = "Copyright 2018, Planet Earth"


class Utility(object):
    """Utility tools class."""

    def __init__(self):
        pass

    @staticmethod
    def is_config_exist():
        config_path = None
        stamp = 0
        path = "config.json"

        if "CONFIG_PATH" in os.environ:
            config_path = os.environ["CONFIG_PATH"]
        elif os.path.exists("./config/" + path):
            config_path = "./config/" + path
        elif os.path.exists("./snmp_collector/config/" + path):
            config_path = "./snmp_collector/config/" + path
        elif os.path.exists(path):
            config_path = path
        elif os.path.exists("../" + path):
            config_path = "../" + path
        elif os.path.exists("../../" + path):
            config_path = "../../" + path
        else:
            log.err("Cannot find a config file!")

        if config_path is not None:
            stamp = os.stat(config_path).st_mtime

        return config_path, stamp


class MWT(object):
    """Memoize With Timeout CACHE as a decorator"""

    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}

            for key in self._caches[func]:

                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = kwargs.items()
            kw = sorted(kw)
            key = (args, tuple(kw))

            try:
                v = self.cache[key]

                if (time.time() - v[1]) > self.timeout:
                    raise KeyError

            except KeyError:
                v = self.cache[key] = f(*args, **kwargs), time.time()

            return v[0]

        func.__name__ = f.__name__

        return func
