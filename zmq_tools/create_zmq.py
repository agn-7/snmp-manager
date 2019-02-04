import zmq
from zmq.auth.thread import ThreadAuthenticator

__author__ = 'Khashayar & aGn'


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
        self.port = None

    def _create_zmq(self, zmq_type, ip, port):
        context = zmq.Context()
        # context = zmq.Context.instance()  # TODO

        auth = ThreadAuthenticator(context)
        auth.start()
        # auth.allow('127.0.0.1')
        auth.configure_plain(domain='*', passwords={'admin': 'admin'})

        self.socket = context.socket(zmq_type)
        self.ip = ip
        self.port = port
        zmq_address = f"tcp://{ip}:{port}"
        self.socket.connect(zmq_address)

    def get_zmq_client(self, zmq_type, ip, port):
        """

        :param zmq_type: Type of ZMQ
        :param ip: ZMQ IP
        :param port: ZMQ Port
        :return: A ZMQ socket.
        """
        if self.socket and self.ip == ip and self.port == port:
            return self.socket

        else:
            self._create_zmq(zmq_type=zmq_type, ip=ip, port=port)
            return self.socket


def make_socket(ip, port):
    con = zmq.Context()
    sock = con.socket(zmq.PUB)
    adrs = f"tcp://{ip}:{port}"
    sock.connect(adrs)
    return sock
