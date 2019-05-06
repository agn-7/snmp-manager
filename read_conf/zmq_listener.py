import zmq
import time
import json
import os
import traceback

from pprint import pprint

from utility.logger import Logging

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

    def always_listen(self, method='REP'):
        """
        Always Listen to the ZMQ from Django side to get the configuration then
        calling .store_config_file() method.
        :return:
        """
        while True:
            if self.socket_zmq:
                print("ZMQ is waiting ...")
                configs = self.socket_zmq.recv_json()
                pprint(configs)
                self.socket_zmq.send_json({'status': 200})  # TODO :: maybe placed in else state.
                self.store_config_file(configs)

            else:
                self.get_zmq(method)

    def get_zmq(self, method='REP'):
            try:
                context = zmq.Context()

                if method == 'PULL':
                    self.socket_zmq = context.socket(zmq.PULL)

                elif method == 'SUB':
                    self.socket_zmq = context.socket(zmq.SUB)
                    self.socket_zmq.setsockopt(zmq.SUBSCRIBE, b'')

                elif method == 'REP':
                    self.socket_zmq = context.socket(zmq.REP)

                else:
                    raise NotImplementedError()

                # self.socket_zmq.setsockopt(zmq.RCVHWM, 1)
                self.socket_zmq.setsockopt(zmq.CONFLATE, 1)  # last msg only.
                print('The Listener Initialized.')
                self.socket_zmq.bind("tcp://*:6668")

            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    logger.captureMessage('state changed since poll event')
                else:
                    logger.captureMessage("RECV Error: %s" % zmq.strerror(e.errno))
                time.sleep(5)

            except Exception as exc:
                print(exc)
                logger.captureMessage(traceback.format_exc())
                self.socket_zmq.close()
                context.destroy()
                time.sleep(5)
