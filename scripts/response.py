from .logger import Logging
from scripts.redis_response import RedisResponse
from scripts.influx_response import InfluxResponse


__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()

PIPELINE = [
    RedisResponse(
        server_ip='127.0.0.1',
        pipeline_ip='127.0.0.1',
        pipeline_port=6677
    ),
    InfluxResponse(
        server_ip='127.0.0.1',
        pipeline_ip='127.0.0.1',
        pipeline_port=9001
    ),
]  # TODO :: Make it dynamically.


class Response(object):
    def __init__(self):
        pass

    @staticmethod
    def publish(  # TODO
            module, meta_data, # *,
            # server_ip='127.0.0.1', pipeline_ip='127.0.0.1', pipeline_port=9001,
            **kwargs
    ):
        for pipe in PIPELINE:
            pipe.publish(  # TODO
                module, meta_data,
                # server_ip=server_ip, pipeline_ip=pipeline_ip, pipeline_port=pipeline_port,
                **kwargs
            )
