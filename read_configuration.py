import json

from pprint import pprint
from easydict import EasyDict as edict

from logger import Logging
from utility import MWT

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


def flatten(configs):
    """
    Parsing the received Json config file.
    :param configs: Received configs from Django admin.
    :return:
    """
    flatten_configs = []

    for conf in configs:
        parent = {}

        for key, val in conf.items():

            if key != "metrics":
                parent[key] = val

            else:

                for met in conf[key]:
                    flatten_configs.append({})

                    for mk, mv in met.items():
                        last_index = len(flatten_configs) - 1
                        flatten_configs[last_index][mk] = mv
                        flatten_configs[last_index].update(parent)

    return flatten_configs


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

        configs = flatten(configs)
        # pprint(configs)

    except Exception as exc:
        logger.captureMessage(exc)
        logger.captureException()

    return configs


if __name__ == '__main__':
    '''Test case usage.'''
    configs = get_config()

    for conf in configs:
        pprint(conf)
