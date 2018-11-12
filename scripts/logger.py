from raven import Client

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class Logging(object):
    def __init__(self):
        pass

    @staticmethod
    def sentry_logger():
        return Client(
            'http://3bb6148d072c4b3ba3dd1415a68cdd3d@192.168.1.131:9000/20'
        )
