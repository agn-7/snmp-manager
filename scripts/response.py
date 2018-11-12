import abc

from abc import abstractmethod

from .logger import Logging
from scripts.redis_pipeline import RedisPipeline
from scripts.influx_pipeline import InfluxPipeline


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()

PIPELINE = [RedisPipeline(), InfluxPipeline()]  # TODO :: Make it dynamically.


class ResponseAbstract(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def publish(
            self, module, meta_data, *,
            server_ip='127.0.0.1', pipeline_ip='127.0.0.1', pipeline_port=9001,
            **kwargs):
        pass


class Response(object):
    def __init__(self):
        pass

    @staticmethod
    def publish(
            module, meta_data, *,
            server_ip='127.0.0.1', pipeline_ip='127.0.0.1', pipeline_port=9001,
            **kwargs
    ):
        for pipe in PIPELINE:
            pipe.publish(
                module, meta_data,
                server_ip=server_ip, pipeline_ip=pipeline_ip, pipeline_port=pipeline_port,
                **kwargs
            )
