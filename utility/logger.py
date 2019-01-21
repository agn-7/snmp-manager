from raven import Client

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
            },
        },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
            },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': 'http://e627c6d4737d4970a095e2b5c95a0269:7fca1cacbfdd4d2298618663668faba0@192.168.1.136/2',
            },
        },

    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': False,
            },
        'your_app': {  # TODO
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


class Logging(object):
    """Sentry Logging Class."""
    def __init__(self):
        pass

    @staticmethod
    def sentry_logger():
        """Sentry logger."""
        return Client(
            'http://3c50d4696400490daa1781671331221b@192.168.1.136/5'
        )
