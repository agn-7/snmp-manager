import zmq

from datetime import datetime
from time import sleep
from pprint import pprint

from utility.logger import Logging
from response.response_abstract import ResponseAbstract


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class InfluxResponse(ResponseAbstract):
    def __init__(self, server_ip, pipeline_ip, pipeline_port):
        super().__init__()

        self.server_ip = server_ip
        self.pipeline_ip = pipeline_ip
        self.pipeline_port = pipeline_port

        context = zmq.Context()
        socket = context.socket(zmq.PUB)

        if self.pipeline_ip != '127.0.0.1':
            zmq_address = "tcp://{}:{}".format(self.pipeline_ip, self.pipeline_port)

        else:
            zmq_address = "tcp://{}:{}".format(self.server_ip, self.pipeline_port)

        socket.connect(zmq_address)
        self.socket = socket

    def publish(
            self, module, meta_data,
            **kwargs
    ):
        """
        Packing Json file in order to sending on ZMQ pipeline.
        :param config: B.M received config.
        :param module:
        :param meta_data:
        :param server_ip: Server_IP
        :param pipeline_ip: Pipeline_IP
        :param pipeline_port: Pipeline_IP
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
                logger.captureMessage('Space if full >> {}'.format(exc))
                sleep(1)

            # sleep()  # TODO :: maybe need a bit sleeping time.
