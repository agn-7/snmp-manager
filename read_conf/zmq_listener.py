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

        try:
            context = zmq.Context()

            if method == 'PULL':
                sock = context.socket(zmq.PULL)

            elif method == 'SUB':
                sock = context.socket(zmq.SUB)
                sock.setsockopt(zmq.SUBSCRIBE, b'')

            elif method == 'REP':
                sock = context.socket(zmq.REP)

            else:
                raise NotImplementedError()

            # sock.setsockopt(zmq.RCVHWM, 1)
            sock.setsockopt(zmq.CONFLATE, 1)  # last msg only.
            print('Listener Initialized.')
            sock.bind("tcp://*:6669")

        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                print('state changed since poll event')
            else:
                print("RECV Error: %s" % zmq.strerror(e.errno))

            self.always_listen(method)  # Recursive.

        while True:
            print('Waiting for json configs ...')

            if sock:
                print('Before recv')

                try:
                    configs = sock.recv_json()
                    '''Get the Battery-Monitoring json configs.'''

                    print('Configurations received.')
                    self.store_config_file(configs)
                    print('Config stored in the config.json file.')

                    if method is 'REP':
                        sock.send_json({'status': 200})

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
