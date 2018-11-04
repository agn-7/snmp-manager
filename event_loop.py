import asyncio
import uvloop

from logger import Logging
from read_configuration import get_config
from collector import SNMPReader

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class EventLoop(object):
    def __init__(self):
        self.loop = None
        self.snmp_reader = SNMPReader()

    def init_loop(self, configs):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        '''Set the uvloop policy.'''

        loop = asyncio.get_event_loop()

        for conf in configs:
            asyncio.ensure_future(
                self.snmp_reader.read(oid=conf['oid'], time=conf['time'])
            )

        return loop

    def run_forever(self):
        configs = get_config()

        if configs:
            loop = self.init_loop(configs)

            try:
                loop.run_forever()

            except KeyboardInterrupt:
                pass

            finally:
                print("Closing Loop")
                loop.close()

        else:
            raise NotImplementedError()


if __name__ == '__main__':
    snmp_configurations = [
        {'time': 5, 'oid': '1.3.6.3.2.4'},
        {'time': 6, 'oid': '1.3.6.3.5.8'},
    ]  # TODO :: DUMMY
    loop = EventLoop().init_loop(snmp_configurations)

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()
