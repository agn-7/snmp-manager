import zmq
import time

from datetime import datetime
from pprint import pprint

from .logger import Logging
from scripts.response_abstract import ResponseAbstract


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class RedisResponse(ResponseAbstract):
    def __init__(self, server_ip, pipeline_ip, pipeline_port):
        super().__init__()
        self.socket = None
        self.server_ip = server_ip
        self.pipeline_ip = pipeline_ip
        self.pipeline_port = pipeline_port

    # def create_pub_socket(self, ip, port):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        zmq_address = "tcp://{}:{}".format(self.pipeline_ip, self.pipeline_port)
        socket.connect(zmq_address)
        self.socket = socket

        # return socket

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
            if self.pipeline_ip != '127.0.0.1':
                # sock = self.create_pub_socket(self.pipeline_ip, self.pipeline_port)
                # sock.send_json(result, flags=0)
                try:
                    self.socket.send_json(result, flags=zmq.NOBLOCK)  # TODO
                except zmq.ZMQError as exc:
                    print('Space if full >> {}'.format(exc))
                    time.sleep(1)

            else:
                print(self.pipeline_port)
                # self.create_pub_socket(self.server_ip, self.pipeline_port)

                if self.socket is not None:
                    # sock.send_json(result, flags=0)
                    try:
                        self.socket.send_json(result, flags=zmq.NOBLOCK)  # TODO
                    except zmq.ZMQError as exc:
                        print('Space if full >> {}'.format(exc))
                        time.sleep(1)

                else:
                    print('There is not any socket')
                # time.sleep(1e-1)  # TODO :: maybe need a bit sleeping time.
