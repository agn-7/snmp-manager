import os

from raven import Client
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class Logging(object):
    """Sentry Logging Class."""
    def __init__(self):
        pass

    @staticmethod
    def sentry_logger():
        """Sentry logger."""
        if 'SENTRY_DSN' in os.environ:
            return Client()
        else:
            return Client(
                'http://ad6aaf5ed24f4de5902db8daf653330d@192.168.1.136/6'
            )

    def init_sentry_with_level(self):
        """
        Initiate Sentry logging with the several pre-defined level in logging library.
        The valid level for sentry is: fatal, critical, error, warning, and exception.
        :return:
        """
        handler = SentryHandler(self.sentry_logger())
        setup_logging(handler)

