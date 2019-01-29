import json
import os
import zmq

from pprint import pprint
from easydict import EasyDict as edict

from utility.logger import Logging
from utility.utility import MWT
from zmq_tools import create_zmq

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


def make_unit_socket(all_config):
    """
    Make unit socket per each IP+Port
    :param all_config: Configuration.
    :return: A dict which is contain to IP+Port key and unit socket value.
    """
    iport = {}
    for conf in all_config:
        for serv in conf['servers']:
            iport[f"{serv['ip']}:{serv['port']}"] = create_zmq.CreateZMQ().get_zmq_client(
                zmq.PUB, serv['ip'], serv['port']
            )

    return iport


def find_its_socket(iport_str, **iport_dict):
    """
    Find the desired socket per each IP+Port.
    :param iport_str: IP+Port
    :param iport_dict: A dict which is contain to IP+Port key and unit socket value.
    :return: Desired socket.
    """
    return iport_dict.get(iport_str)


def add_socket(all_config):
    """
    Add socket key value to the servers in the configuration list of dict.
    :param all_config: Configuration.
    :return: Updated configuration with socket key value the in servers key.
    """
    iport = make_unit_socket(all_config)

    for conf in all_config:
        for serv in conf['servers']:
            serv['socket'] = find_its_socket(f"{serv['ip']}:{serv['port']}", **iport)

    return all_config


@MWT(timeout=7)
def get_config():
    """
    Reading the stored SNMP Json configuration file.
    :return: SNMP configuration Json.
    """
    configs = None

    try:
        if 'CONFIG_PATH' in os.environ:
            config_path = os.environ['CONFIG_PATH']
        elif os.path.exists("/app/config.json"):
            config_path = '/app/config.json'
        elif os.path.exists("../config.json"):
            config_path = '../config.json'
        elif os.path.exists("config.json"):
            config_path = 'config.json'
        else:
            raise ValueError("Cannot find a config file!")

        with open(config_path) as json_file:
            configs = json.load(json_file)
            configs = flatten(configs)
            configs = add_socket(configs)
            pprint(configs)

    except (KeyError, IOError, FileNotFoundError, Exception) as exc:
        logger.captureMessage(exc)
        logger.captureException()

    return configs


if __name__ == '__main__':
    '''Test case usage.'''
    configs = get_config()

    for conf in configs:
        pprint(conf)
