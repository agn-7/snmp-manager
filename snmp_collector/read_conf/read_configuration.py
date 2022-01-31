import json
import os

from pprint import pprint
from pysnmp.hlapi.asyncio import *
from colored_print import ColoredPrint

try:
    from snmp_collector.utility.utility import MWT
except:
    from utility.utility import MWT
    
log = ColoredPrint()

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


def flatten(configs):
    """
    Parsing the received Json config file (removing metrics key and spread them in parent key).
    :param configs: Received configs from Django admin.
    :return:
    """
    flatten_configs = []

    for conf in configs:
        parent = {}

        for key, val in conf.items():
            if key != "metrics":
                parent[key] = val

        for key, val in conf.items():
            if key == 'metrics':
                for met in conf[key]:
                    flatten_configs.append({})
                    last_index = len(flatten_configs) - 1
                    flatten_configs[last_index].update(parent)

                    for mk, mv in met.items():
                        flatten_configs[last_index][mk] = mv

    return flatten_configs


def parse_isEnable(configs):
    """
    Set isEnable=False to each parameter isEnable if its parent (SNMP device) isEnable key ,equal
    to False.
    :param configs: SNMP configurations.
    :return: Applied isEnable from SNMP device config to each SNMP parameters.
    """
    for conf in configs:
        if not conf['isEnable']:
            for metric in conf['metrics']:
                metric['isEnable'] = False

    return configs


def add_snmp_engine(configs):
    """
    Add SNMP-Engine per each SNMP-Line or SNMP-Device.
    :param configs: flatten SNMP configurations.
    :return: Updated configuration with SNMP-Engine key value.
    """
    for conf in configs:
        conf['engine'] = SnmpEngine()

    return configs


# @MWT(timeout=7)
def get_config():
    """
    Reading the stored SNMP Json configuration file.
    :return: SNMP configuration Json.
    """
    configs = None

    try:
        if 'CONFIG_PATH' in os.environ:
            config_path = os.environ['CONFIG_PATH']
        elif os.path.exists("/app/config/config.json"):
            config_path = '/app/config/config.json'
        elif os.path.exists("../config.json"):
            config_path = '../config.json'
        elif os.path.exists("config.json"):
            config_path = 'config.json'
        elif os.path.exists("./config/config.json"):
            config_path = './config/config.json'
        elif os.path.exists("./snmp_collector/config/config.json"):
            config_path = './snmp_collector/config/config.json'  
        else:
            raise ValueError("Cannot find a config file!")

        with open(config_path) as json_file:
            configs = json.load(json_file)
            configs = parse_isEnable(configs)
            configs = add_snmp_engine(configs)
            configs = flatten(configs)
            pprint(configs)

    except (KeyError, IOError, FileNotFoundError, Exception) as exc:
        log.err(exc)

    return configs


if __name__ == '__main__':
    '''Test case usage.'''
    configs = get_config()

    for conf in configs:
        pprint(conf)
