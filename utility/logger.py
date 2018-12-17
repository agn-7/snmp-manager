from raven import Client

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class Logging(object):
    def __init__(self):
        pass

    @staticmethod
    def sentry_logger():
        return Client(
            'http://e627c6d4737d4970a095e2b5c95a0269:7fca1cacbfdd4d2298618663668faba0@192.168.1.136/2'
        )
