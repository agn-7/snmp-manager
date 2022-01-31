from datetime import datetime
from colored_print import ColoredPrint

log = ColoredPrint()

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


class Response(object):
    """Response Class"""
    def __init__(self):
        self.socket = None

    @staticmethod
    def publisher(
            module, meta_data,
            **kwargs
    ):
        """
        Packing Json file in order to sending on ZMQ pipeline.
        :param module:
        :param meta_data:
        :param kwargs: SNMP values result.
        :return:
        """
        for name, data in kwargs.items():
            if data != -8555:
                meta_data['status'] = 200
            else:
                meta_data['status'] = 404

            result = {
                'data': {name: data},
                'module': module,
                'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'station': 'SNMP',
                'tags': meta_data
            }

            log.success({name: data}, ' ', result['time'])

    def publish(
            self,
            module, meta_data,
            **kwargs
    ):
        """
        Call the publisher method to send the result on the subscriber servers by ZMQ.
        :param module:
        :param meta_data:
        :param kwargs:
        :return:
        """
        self.publisher(
            module, meta_data,
            **kwargs
        )
