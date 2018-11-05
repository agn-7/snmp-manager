import ast
import json
import asyncio

from time import sleep
from easydict import EasyDict as edict
from multiprocessing import Process
from easysnmp import snmp_get

from response import Response
from logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class SNMPReader(object):
    def __init__(self):
        pass

    async def read(self, **kwargs):
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        name = kwargs.get('tag_name', 'Default Name')
        address = kwargs.get('address', 1)
        community = kwargs.get('community', 'public')
        version = kwargs.get('version', 1)
        port = kwargs.get('port', 161)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 1)

        try:
            data = float(
                snmp_get(  # TODO :: Check the await.
                    oid,
                    hostname=address,
                    community=community,
                    version=version,
                    remote_port=port,
                    timeout=timeout,
                    retries=retries,
                ).value
            )

            print(name, data)
            return {name: data}

        except Exception as exc:
            print(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    exc
                )
            )
            logger.captureMessage(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    exc
                )
            )

            return {name: None}

        finally:
            await asyncio.sleep(interval)

    def process(self, config, **kwargs):
        """
        Reading desired values from Shahab's board.
        :param config: Received Json-configs.
        :return:
        """

        server_ip = kwargs.get('server_ip')
        pipeline_ip = kwargs.get('pipeline_ip')
        pipeline_port = kwargs.get('pipeline_port')
        # print(result)

        self.response.publish(
            config,
            server_ip=server_ip,
            pipeline_ip=pipeline_ip,
            pipeline_port=pipeline_port,
            **result
        )
        flag = True

    def async_parser(self, configs):
        """
        Async multiprocess Parsing the received Json config file and call the .process() method.
        :param configs: Received configs from Django admin.
        :return:
        """
        jobs = list()
        obj_config = edict(configs)
        kwargs = dict(server_ip=obj_config._server_ip,
                      pipeline_ip=obj_config._pipeline_ip,
                      pipeline_port=obj_config._pipeline_port)

        if obj_config._start:

            for dongle in obj_config._dongles:
                cli = self.set_client(dongle)
                job = Process(target=self.async_sub_process, args=(dongle, cli), kwargs=kwargs)
                jobs.append(job)
                job.start()

            for j in jobs:
                j.join()

        else:
            print('BM config starter is OFF.')
            sleep(1)

