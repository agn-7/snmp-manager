import zmq

from pprint import pprint
from datetime import datetime
from time import sleep

from utility.logger import Logging


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class Response(object):
    def __init__(self):
        self.socket = None

    def publisher(
            self,
            module, meta_data,
            **kwargs
    ):
        """
        Packing Json file in order to sending on ZMQ pipeline.
        :param config: B.M received config.
        :param module:
        :param meta_data:
        :param kwargs: Battery values result.
        :return:
        """
        for name, data in kwargs.items():
            result = {
                'data': {name: data},
                'module': module,
                'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'station': 'SNMP',
                'tags': meta_data
            }

            pprint(result)  # TODO :: make it to the logger if is necessary.

            try:
                self.socket.send_json(result, flags=zmq.NOBLOCK)  # TODO

            except zmq.ZMQError as exc:
                print('Space if full >> {}'.format(exc))
                sleep(1)

            # sleep()  # TODO :: maybe need a bit sleeping time.

    def publish(
            self,
            module, meta_data, servers,
            **kwargs
    ):

        for server in servers:
            context = zmq.Context()
            socket = context.socket(zmq.PUB)
            zmq_address = "tcp://{}:{}".format(server.ip, server.port)
            socket.connect(zmq_address)
            self.socket = socket

            self.publisher(
                module, meta_data,
                **kwargs
            )

