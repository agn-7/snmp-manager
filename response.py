import zmq

from datetime import datetime
from time import sleep
from logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class Response(object):
    def __init__(self):
        # self.pub_socket = self.create_pub_socket()
        pass

    @staticmethod
    def create_pub_socket(ip, port):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        zmq_address = "tcp://{}:{}".format(ip, port)
        socket.connect(zmq_address)

        return socket

    def publish(
            self, module, meta_data, *,
            server_ip='127.0.0.1', pipeline_ip='127.0.0.1', pipeline_port=9001,
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

            print(result)  # TODO :: make it to the logger if is necessary.
            if pipeline_ip != '127.0.0.1':
                sock = self.create_pub_socket(pipeline_ip, pipeline_port)
                # sock.send_json(result, 0)
                sock.send_json(result, flags=zmq.NOBLOCK)  # TODO

            else:
                sock = self.create_pub_socket(server_ip, pipeline_port)
                # sock.send_json(result, 0)
                sock.send_json(result, flags=zmq.NOBLOCK)  # TODO

            # sleep()  # TODO :: maybe need a bit sleeping time.
