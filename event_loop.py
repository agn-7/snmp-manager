import asyncio
import uvloop
import async_timeout

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

    @staticmethod
    def get_timeout(sleep, timeout):
        if sleep < timeout:
            total_time = sleep + timeout

        else:
            total_time = max(sleep, timeout)

        return total_time + .1  # TODO

    async def read_forever(self, loop, **kwargs):
        """

        :param loop:
        :param kwargs:
        :return:
        """
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 3)
        total_timeout = self.get_timeout(sleep=interval, timeout=(timeout * retries))

        while True:
            try:
                # async with async_timeout.timeout(total_timeout, loop=loop) as cm:
                async with async_timeout.timeout(total_timeout) as cm:
                    await self.snmp_reader.read(loop, **kwargs)

            except asyncio.TimeoutError as exc:
                # print(cm.expired, exc)
                pass

            except KeyboardInterrupt:
                loop.close()

    def init_loop(self, configs, forever=True):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        '''Set the uvloop event loop policy.'''

        loop = asyncio.get_event_loop()

        if not forever:
            '''Run once.'''
            futures = [asyncio.ensure_future(self.snmp_reader.read(loop, **conf))
                       for conf in configs]

        else:
            '''Run forever.'''
            # futures = [asyncio.ensure_future(self.read_forever(loop, **conf))
            #            for conf in configs]
            '''OR'''
            futures = [loop.create_task(self.read_forever(loop, **conf))
                       for conf in configs]

        return loop, futures

    def run_once(self):
        configs = get_config()

        if configs:
            loop, futures = self.init_loop(configs, forever=False)
            result = loop.run_until_complete(asyncio.gather(*futures))
            print(result)

        else:
            raise NotImplementedError()

    def run_forever(self):
        configs = get_config()

        if configs:
            loop, _ = self.init_loop(configs, forever=True)

            try:
                loop.run_forever()

            except KeyboardInterrupt:
                pass

            finally:
                print("Closing Loop")
                loop.close()

        else:
            raise NotImplementedError()


if __name__ == '__main__':  # TODO :: Test.
    snmp_configurations = [
        {'interval': 5, 'oid': '1.3.6.3.2.4'},
        {'interval': 6, 'oid': '1.3.6.3.5.8'},
    ]  # TODO :: DUMMY
    loop, futures = EventLoop().init_loop(snmp_configurations, forever=True)

    try:
        loop.run_forever()
        # res = loop.run_until_complete(asyncio.gather(*futures))
        # print(res)

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()
