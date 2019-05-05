import zmq
import traceback

from datetime import datetime
from time import sleep

from utility.logger import Logging


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class Response(object):
    """Response Class"""
    def __init__(self):
        self.socket = None

    def publisher(
            self,
            module, meta_data, server,
            **kwargs
    ):
        """
        Packing Json file in order to sending on ZMQ pipeline.
        :param module:
        :param meta_data:
        :param server: server key and value in configuration that has a ZeroMQ socket.
        :param kwargs: Battery values result.
        :return:
        """
        for name, data in kwargs.items():
            if data != -8555:
                meta_data['status'] = 200
            else:
                meta_data['status'] = 404

            result = {
                'data': {name: data},
                'module': module,
                'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'station': 'SNMP',
                'tags': meta_data
            }

            print({name: data}, ' ', result['time'], '-->', server['ip'], ':', server['port'])

            try:
                server['socket'].send_json(result, flags=zmq.NOBLOCK)  # TODO

            except zmq.ZMQError as exc:
                logger.captureMessage(
                    f"Space if full >> {exc}"
                )
                sleep(1)

            except Exception:
                logger.captureMessage(traceback.format_exc())

    def publish(
            self,
            module, meta_data, servers,
            **kwargs
    ):
        """
        Call the publisher method to send the result on the subscriber servers by ZMQ.
        :param module:
        :param meta_data:
        :param servers:
        :param kwargs:
        :return:
        """
        for server in servers:
            self.publisher(
                module, meta_data, server,
                **kwargs
            )

