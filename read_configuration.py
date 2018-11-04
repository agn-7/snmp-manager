import json

from logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


def get_config():
    """
    Reading the stored SNMP Json configuration file.
    :return: SNMP configuration Json.
    """
    configs = None

    try:
        with open('config.json') as json_file:
            configs = json.load(json_file)
            print(configs)

    except Exception as exc:
        logger.captureMessage(exc)
        logger.captureException()

    return configs
