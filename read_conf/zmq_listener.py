import zmq
import time
import json

from utility.logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class Getter(object):
    def __init__(self):
        self.socket_zmq = None

    @staticmethod
    def store_config_file(config):
        """
        Write and store received BM Json config to a file.
        :param config: Received BM Json config from Django side.
        :return:
        """
        print('writer', config)

        try:
            with open('config.json', 'w') as outfile:
                json.dump(config, outfile)

        except Exception as exc:
            logger.captureMessage(exc)

    def always_listen(self, method='PULL'):
        """
        Always listen to the ZMQ.SNDER from Django side to get the SNMP configuration then calling
        the .store_config_file() method.
        :return:
        """
        sock = None
        print('In listener')

        try:
            context = zmq.Context()

            if method == 'PULL':
                print('In pull')
                sock = context.socket(zmq.PULL)

            elif method == 'SUB':
                print('In sub')
                sock = context.socket(zmq.SUB)
                sock.setsockopt(zmq.SUBSCRIBE, b'')

            elif method == 'REP':
                if self.socket_zmq is not None:
                    print("ZMQ is waiting for config...")
                    configs = self.socket_zmq.recv_json()
                    self.socket_zmq.send_json({'status': 200})
                    self.store_config_file(configs)
                    self.always_listen(method='REP')  # Recursive

                else:
                    self.get_zmq()
                    self.always_listen(method='REP')  # Recursive

            else:
                raise NotImplementedError()

            # sock.setsockopt(zmq.RCVHWM, 1)
            sock.setsockopt(zmq.CONFLATE, 1)  # last msg only.
            print('Listener Initialized.')
            sock.bind("tcp://*:6669")  # TODO :: before was 6667

        except zmq.ZMQError:
            logger.captureException()

        while True:
            print('Waiting for json configs ...')

            if sock:
                print('Before recv')

                try:
                    configs = sock.recv_json()
                    print('After recv')
                    '''Get the Battery-Monitoring json configs.'''

                    time.sleep(1e-1)
                    print('BM Configurations received.')
                    self.store_config_file(configs)
                    print('BM Config stored in the config.json file.')

                except zmq.ZMQError as e:
                    if e.errno == zmq.EAGAIN:
                        print('state changed since poll event')

                    else:
                        print("RECV Error: %s" % zmq.strerror(e.errno))

            else:
                print('An error occurred in ZMQ socket creation.')
                logger.captureMessage('An error occurred in ZMQ socket creation.')
                time.sleep(5)
                self.always_listen(method)  # Recursive.

    def listen(self, method='PULL'):
        """
        Listen to the ZMQ.PUSH from Django side to get the BM configuration then calling .store_config_file() method.
        :return:
        """
        sock = None

        try:
            context = zmq.Context()

            if method == 'PULL':
                sock = context.socket(zmq.PULL)

            elif method == 'SUB':
                sock = context.socket(zmq.SUB)
                sock.setsockopt(zmq.SUBSCRIBE, b'')

            else:
                raise NotImplementedError()

            # sock.setsockopt(zmq.RCVHWM, 1)
            sock.setsockopt(zmq.CONFLATE, 1)  # last msg only.
            print('Listener Initialized.')
            # logger.captureMessage('Listener Initialized.')
            sock.bind("tcp://*:6667")

        except zmq.ZMQError:
            logger.captureException()

        configs = None

        while configs is None:
            print('Waiting for json configs ...')

            if sock:
                configs = sock.recv_json(flags=zmq.NOBLOCK)
                '''Get the Battery-Monitoring json configs.'''
                time.sleep(1e-1)

            else:
                logger.captureMessage('An error occurred in ZMQ socket creation.')
                time.sleep(5)
                self.listen(method)  # Recursive.

        print('BM Configurations received.')
        self.store_config_file(configs)
        print('BM Config stored in the config.json file.')

    def get_zmq(self):
        if not self.socket_zmq:
            context = zmq.Context()
            self.socket_zmq = context.socket(zmq.REP)
            self.socket_zmq.bind("tcp://*:6669")
