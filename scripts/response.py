from abc import ABC, abstractmethod

from .logger import Logging
from scripts.redis_pipeline import RedisPipeline
from scripts.influx_pipeline import InfluxPipeline


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()

PIPELINE = [
    RedisPipeline(
        server_ip='127.0.0.1',
        pipeline_ip='127.0.0.1',
        pipeline_port=9002
    ),
    InfluxPipeline(
        server_ip='127.0.0.1',
        pipeline_ip='127.0.0.1',
        pipeline_port=9001
    ),
]  # TODO :: Make it dynamically.


class ResponseAbstract(ABC):
    def __init__(
            self,
            server_ip='127.0.0.1',
            pipeline_ip='127.0.0.1',
            pipeline_port=9001
    ):
        self.server_ip = server_ip
        self.pipeline_ip = pipeline_ip
        self.pipeline_port = pipeline_port
        super().__init__()

    @abstractmethod
    def publish(
            self, module, meta_data,
            **kwargs
    ):
        pass


class Response(object):
    def __init__(self):
        pass

    @staticmethod
    def publish(  # TODO
            module, meta_data, *,
            server_ip='127.0.0.1', pipeline_ip='127.0.0.1', pipeline_port=9001,
            **kwargs
    ):
        for pipe in PIPELINE:
            pipe.publish(  # TODO
                module, meta_data,
                # server_ip=server_ip, pipeline_ip=pipeline_ip, pipeline_port=pipeline_port,
                **kwargs
            )
