import ast
import json

from time import sleep
from pymodbus.client.sync import ModbusSerialClient
from easydict import EasyDict as edict
from multiprocessing import Process

from tag_generator import TagGenerator
from response import Response
from logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class BatteryMonitoringReader(TagGenerator):
    def __init__(self):
        super().__init__()
        self.client = None
        self.response = Response()

    def set_client(self, config):
        """Modbus client creator."""
        try:
            cli = ModbusSerialClient(
                method=config._method,
                port=config._com,
                baudrate=config._baud_rate,
                timeout=config._time_out,
                parity=config._parity,
                stopbits=config._stop_bits,
                bytesize=config._byte_size
            )
            self.client = cli

            return cli

        except Exception as exc:
            print(exc)
            logger.captureMessage(exc)

            return False

    def connect_(self, client=None):
        """
        Connect to the defined port/com.
        :param client: RS485 Client.
        :return: Status.
        """
        if client is not None:
            if not client:
                try:
                    return client.connect()

                except Exception as err:
                    logger.captureMessage(err)
                    logger.captureException()
                    return False

            else:
                return True

        else:
            if not self.client:
                try:
                    return self.client.connect()

                except Exception as err:
                    logger.captureMessage(err)
                    logger.captureException()
                    return False
            else:
                return True

    def close_(self):
        """Close the connection."""
        self.client.close()

    @staticmethod
    def get_config():
        """
        Reading the stored BM Json configuration file.
        :return: BM configuration Json.
        """
        configs = None

        try:
            with open('config.json') as json_file:
                configs = json.load(json_file)
                print(configs)

        except Exception as exc:
            logger.captureMessage(exc)
            logger.captureException()

        return configs

    def read_register(self, address, unit=1, count=1, **kwargs):
        """Modbus reading holding registers"""
        return self.client.read_holding_registers(address, count, unit=unit, **kwargs)

    def response_handler(self, *args):
        """
        Getting the registers (values) from returned modbus holding register object.
        :param args: BM results.
        :return: Registers.
        """
        result = None

        if len(args) == 1:

            if not args[0].isError():
                '''isError() method implemented in pymodbus 1.5.1 and above'''

                result = args[0].registers

            else:
                logger.captureMessage('Unable to read from the battery monitoring device or connection problem. #1')

        elif len(args) == 2:

            if not args[0].isError() and not args[1].isError():
                '''isError() method implemented in pymodbus 1.5.1 and above'''

                result = args[0].registers + args[1].registers

            else:
                self.close_()
                sleep(1)
                self.connect_()
                logger.captureMessage('Unable to read from the battery monitoring device or connection problem. #2')

        else:
            logger.captureMessage('Maximum response_handler() arguments is 2.')

        return result

    def process(self, config, **kwargs):
        """
        Reading desired values from Shahab's board.
        :param config: Received Json-configs.
        :return:
        """
        flag = None
        print('In process')

        try:
            generated_tags = self.define_registers(config)
            result = generated_tags
            min_address = min(generated_tags, key=generated_tags.get)
            max_address = max(generated_tags, key=generated_tags.get)

            count = generated_tags[max_address] - generated_tags[min_address] + 1

            if count < 120:
                res = self.read_register(generated_tags[min_address], count=count, unit=config._unit)
                res_list = self.response_handler(res)

            else:
                logger.captureMessage('Sub battery monitoring device registers is more than 20 sub-modules!')
                raise NotImplementedError()

            if res_list is not None:

                try:
                    '''Compatible with Python3.x version'''

                    for key, reg in generated_tags.items():
                        '''Inserting each value to the considered tag.'''

                        result[key] = res_list[reg]

                except:
                    '''Compatible with Python2 version'''

                    for key, reg in generated_tags.iteritems():
                        '''Inserting each value to the considered tag.'''

                        result[key] = res_list[reg]

            else:
                logger.captureMessage('Unable to read from the battery monitoring device or connection problem. #3')

                try:
                    '''Compatible with Python3.x version'''

                    for key, reg in generated_tags.items():
                        '''Init each values of tags with a dummy value.'''

                        result[key] = -85555
                        '''This is a value in erroneous situation.'''

                except:
                    '''Compatible with Python2 version'''

                    for key, reg in generated_tags.iteritems():
                        '''Init each values of tags with a dummy value.'''

                        result[key] = -85555
                        '''This is a value in erroneous situation.'''

                # return None  # TODO

            server_ip = kwargs.get('server_ip')
            pipeline_ip = kwargs.get('pipeline_ip')
            pipeline_port = kwargs.get('pipeline_port')
            # print(result)

            self.response.publish(
                config,
                server_ip=server_ip,
                pipeline_ip=pipeline_ip,
                pipeline_port=pipeline_port,
                **result
            )
            flag = True

        except Exception as exp:
            self.close_()
            sleep(1)
            self.connect_()
            logger.captureMessage('Unable to read from the battery monitoring device. >> {}'.format(exp))
            logger.captureException()

            flag = False

        finally:
            sleep(config._frequency)

            return flag

    def async_sub_process(self, config, client, **kwargs):
        """
        Sub process per each dongle configuration as async.
        :param config:
        :param client:
        :param kwargs:
        :return:
        """
        jobs = list()

        if self.connect_(client):

            for dev in config['_sub_devices']:
                obj_dev = edict(dev)
                job = Process(target=self.process, args=(obj_dev,), kwargs=kwargs)  # TODO :: Evaluate threading instead
                jobs.append(job)
                job.start()

            for j in jobs:
                j.join()

        else:
            print('An error occurred in connection.')
            sleep(1)

    def sub_process(self, config, client, **kwargs):
        """
        Sub process per each dongle configuration.
        :param config: A dongle configuration.
        :param client: An RS485 client.
        :param kwargs: A dictionary consist of server and pipeline IP/port.
        :return:
        """
        print('In subprocess')
        if self.connect_(client):
            print('In if')

            for dev in config['_sub_devices']:
                obj_dev = edict(dev)
                self.process(obj_dev, **kwargs)

        else:
            print('An error occurred in connection.')
            sleep(1)

    def async_parser(self, configs):
        """
        Async multiprocess Parsing the received Json config file and call the .process() method.
        :param configs: Received configs from Django admin.
        :return:
        """
        jobs = list()
        obj_config = edict(configs)
        kwargs = dict(server_ip=obj_config._server_ip,
                      pipeline_ip=obj_config._pipeline_ip,
                      pipeline_port=obj_config._pipeline_port)

        if obj_config._start:

            for dongle in obj_config._dongles:
                cli = self.set_client(dongle)
                job = Process(target=self.async_sub_process, args=(dongle, cli), kwargs=kwargs)
                jobs.append(job)
                job.start()

            for j in jobs:
                j.join()

        else:
            print('BM config starter is OFF.')
            sleep(1)

    def parser(self, configs):
        """
        Parsing the received Json config file and call the .process() method.
        :param configs: Received configs from Django admin.
        :return:
        """
        jobs = list()
        obj_config = edict(configs)
        kwargs = dict(server_ip=obj_config._server_ip,
                      pipeline_ip=obj_config._pipeline_ip,
                      pipeline_port=obj_config._pipeline_port)

        if obj_config._start:

            for dongle in obj_config._dongles:
                cli = self.set_client(dongle)
                job = Process(target=self.sub_process, args=(dongle, cli), kwargs=kwargs)
                jobs.append(job)
                job.start()

            for j in jobs:
                j.join()

        else:
            print('BM config starter is OFF.')
            sleep(1)

    def run_once(self):
        configs = self.get_config()

        if configs:
            self.parser(configs)
            # self.async_parser(configs)

        else:
            sleep(5)

    def run_forever(self):
        while True:
            self.run_once()
