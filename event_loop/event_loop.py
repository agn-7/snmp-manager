import asyncio
import uvloop
import async_timeout
import time

from utility.logger import Logging
from read_conf.read_configuration import get_config
from collect.collector import SNMPReader
from utility.utility import Utility

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class EventLoop(object):
    def __init__(self):
        self.loop = None
        self.snmp_reader = SNMPReader()
        self.util = Utility()

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
                    await self.snmp_reader.read_async_full(loop, **kwargs)

            except asyncio.TimeoutError as exc:
                # print(cm.expired, exc)
                pass

            except KeyboardInterrupt:
                loop.close()

    def run_once(self):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        '''Set the uvloop event loop policy.'''

        loop = asyncio.get_event_loop()
        configs = get_config()

        if configs:
            futures = [asyncio.ensure_future(self.snmp_reader.read_async_full(loop, **conf))
                       for conf in configs]
            result = loop.run_until_complete(asyncio.gather(*futures))
            print(result)

        else:
            raise NotImplementedError()

    async def restart_loop(self):
        loop = asyncio.get_event_loop()
        _, cache = self.util.is_config_exist()

        while True:
            config_path, stamp = self.util.is_config_exist()

            if stamp != cache:
                cache = stamp
                loop.stop()
                print('Loop Restarted.')

            await asyncio.sleep(10)

    def run_forever(self):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        '''Set the uvloop event loop policy.'''

        loop = asyncio.get_event_loop()
        loop.create_task(self.restart_loop())

        while True:
            print(11111)
            configs = get_config()
            print(configs)
            if configs:
                futures = [loop.create_task(self.read_forever(loop, **conf))
                           for conf in configs]
                try:
                    loop.run_forever()

                    for f in futures:
                        f.cancel()

                except KeyboardInterrupt:
                    loop.close()

                except asyncio.CancelledError:
                    print('Tasks has been canceled')
                    loop.close()

                except Exception as exc:
                    print(exc)

            else:
                time.sleep(5)
                logger.captureMessage("Waiting for SNMP configuration ...")


if __name__ == '__main__':
    EventLoop().run_forever()
