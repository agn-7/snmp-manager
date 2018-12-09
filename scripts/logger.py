from raven import Client

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class Logging(object):
    def __init__(self):
        pass

    @staticmethod
    def sentry_logger():
        return Client(
            'http://28946bed82554da99bd5bc49aecf33bd:6c335d25e7284ebd8dfeab5daed02558@192.168.1.136:9000/3'
        )
