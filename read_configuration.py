import json

from pprint import pprint

from logger import Logging
from utility import MWT

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


@MWT(timeout=7)
def get_config():
    """
    Reading the stored SNMP Json configuration file.
    :return: SNMP configuration Json.
    """
    configs = None

    try:
        with open('config.json') as json_file:
            configs = json.load(json_file)
            pprint(configs)

    except Exception as exc:
        logger.captureMessage(exc)
        logger.captureException()

    return configs


if __name__ == '__main__':
    '''Test case usage.'''
    configs = get_config()

    for conf in configs:
        pprint(conf)
