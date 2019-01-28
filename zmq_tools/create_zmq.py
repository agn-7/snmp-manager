import zmq

__author__ = 'Khashayar'
__email__ = 'khashayar@infravision.ir'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class CreateZMQ(metaclass=Singleton):
    """ZMQ socket Creator which is use Singleton pattern."""
    def __init__(self):
        self.socket = None
        self.ip = None

    def _create_zmq(self, zmq_type, ip, port):
        context = zmq.Context()
        self.socket = context.socket(zmq_type)
        self.ip = ip
        zmq_address = f"tcp://{ip}:{port}"
        self.socket.connect(zmq_address)

    def get_zmq_client(self, zmq_type, ip, port):
        """

        :param zmq_type: Type of ZMQ
        :param ip: ZMQ IP
        :param port: ZMQ Port
        :return: A ZMQ socket.
        """
        if self.socket and self.ip == ip:
            return self.socket

        else:
            self._create_zmq(zmq_type=zmq_type, ip=ip, port=port)
            return self.socket
