from utility.logger import Logging
from response.redis_response import RedisResponse
from response.influx_response import InfluxResponse
from response.raw_response import RawResponse


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
        server_ip='192.168.1.134',
        pipeline_ip='127.0.0.1',
        pipeline_port=9001
    ),
    RawResponse(
        server_ip='127.0.0.1',
        pipeline_ip='127.0.0.1',
        pipeline_port=7766
    )
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