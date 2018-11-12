from abc import ABC, abstractmethod

from .logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


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
