import zmq
import time
import json
import os
import traceback

from utility.logger import Logging
from pprint import pprint

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class Getter(object):
    """SNMP Config Getter."""
    def __init__(self):
        self.socket_zmq = None

    @staticmethod
    def store_config_file(config):
        """
        Write and store received BM Json config to a file.
        :param config: Received BM Json config from Django side.
        :return:
        """
        try:
            if 'CONFIG_PATH' in os.environ:
                config_path = os.environ['CONFIG_PATH']
            elif os.path.exists("./config/config.json"):
                config_path = './config/config.json'
            elif os.path.exists("config.json"):
                config_path = 'config.json'
            elif os.path.exists("../config.json"):
                config_path = '../config.json'
            else:
                '''DUMMY'''
                logger.captureMessage("Cannot find a config file!")
                config_path = 'config.json'

            with open(config_path, 'w') as outfile:
                json.dump(config, outfile)

        except KeyError as ke:
            logger.captureMessage(ke)
            logger.captureException()

        except IOError as ie:
            logger.captureMessage(ie)
            logger.captureException()

        except Exception as exc:
            logger.captureMessage(exc)
            logger.captureException()

    def always_listen(self, method='PULL'):
        """
        Always listen to the ZMQ.SNDER from Django side to get the SNMP configuration then calling
        the .store_config_file() method.
        :return:
        """
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
            print('The Listener Initialized.')
            sock.bind("tcp://*:6669")

            while True:
                print('Waiting for json configs ...')

                if sock:
                    print('Before recv')
                    configs = sock.recv_json()
                    pprint(configs)

                    print('Configurations received.')
                    self.store_config_file(configs)
                    print('Config stored in the config.json file.')

                    if method == 'REP':
                        sock.send_json({'status': 200})

                else:
                    print('An error occurred in ZMQ socket creation.')
                    logger.captureMessage('An error occurred in ZMQ socket creation.')
                    time.sleep(5)
                    self.always_listen(method)  # Recursive.

        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                logger.captureMessage('state changed since poll event')
            else:
                logger.captureMessage("RECV Error: %s" % zmq.strerror(e.errno))

            time.sleep(5)
            self.always_listen(method)  # Recursive.

        except Exception:
            logger.captureMessage(traceback.format_exc())
            self.always_listen(method)  # Recursive.
