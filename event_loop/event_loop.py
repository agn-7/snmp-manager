import asyncio
import uvloop
import async_timeout
import time
import traceback
import sys

from utility.logger import Logging
from read_conf.read_configuration import get_config
from collect.collector import SNMPReader
from utility.utility import Utility

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class EventLoop(object):
    """AsyncIO EventLoop"""
    def __init__(self):
        self.loop = None
        self.snmp_reader = SNMPReader()
        self.util = Utility()

    @staticmethod
    def get_timeout(sleep, timeout):
        """
        Set a trusted timeout with gathering the sleep time and the timeout.
        :param sleep: Declared sleep.
        :param timeout: Declared timeout
        :return: Trusted Timeout.
        """
        if sleep < timeout:
            total_time = sleep + timeout

        else:
            total_time = max(sleep, timeout)

        return total_time + .1  # TODO

    async def read_forever(self, loop, **kwargs):
        """
        Forever worker to collecting the SNMP(s) device.
        :param loop: asyncio loop.
        :param kwargs: The below parameters.
        :return:
        """
        # timeout = kwargs.get('timeout', 1)
        # retries = kwargs.get('retries', 3)
        # interval = kwargs.get('sleep_time', 3)
        # total_timeout = self.get_timeout(sleep=interval, timeout=(timeout * retries))

        while True:
            try:
                # async with async_timeout.timeout(total_timeout) as cm:
                await self.snmp_reader.read_async_full(loop, **kwargs)

            # except asyncio.TimeoutError as exc:
            #     print(cm.expired, exc)
            #     pass

            except KeyboardInterrupt:
                loop.close()

    def run_once(self):
        """Run once method in asyncio tech."""

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
        """An asynchronous loop re-starter worker to monitor the change in the config file."""
        loop = asyncio.get_event_loop()
        _, cache = self.util.is_config_exist()

        while True:
            config_path, stamp = self.util.is_config_exist()

            if stamp != cache:
                cache = stamp
                print('Loop will be restarted.')
                loop.stop()

            await asyncio.sleep(10)

    @staticmethod
    def stop_auth(configs):
        for conf in configs:
            for srv in conf['servers']:
                try:
                    srv['auth'].stop
                except Exception as exc:
                    logger.captureMessage(exc)

    def run_forever(self):
        """Forever event-loop with the loop re-starter ability in asyncio tech."""

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        '''Set the uvloop event loop policy.'''

        loop = asyncio.get_event_loop()
        loop.create_task(self.restart_loop())

        while True:
            configs = get_config()
            if configs:
                futures = []
                for conf in configs:
                    if conf['isEnable']:
                        futures.append(loop.create_task(self.read_forever(loop, **conf)))

                    else:
                        info_ = f"{conf['name']} SNMP-Model is Disable."
                        logger.captureMessage(info_)

                # futures = [loop.create_task(self.read_forever(loop, **conf))
                #            for conf in configs]
                try:
                    loop.run_forever()
                    self.stop_auth(configs)

                    for f in futures:
                        f.cancel()

                except KeyboardInterrupt:
                    logger.captureMessage("The process was killed.")
                    loop.close()

                except asyncio.CancelledError:
                    logger.captureMessage('Tasks has been canceled')
                    loop.close()
                    sys.exit(0)

                except Exception:
                    logger.captureMessage(traceback.format_exc())

            else:
                time.sleep(5)
                logger.captureMessage("Waiting for SNMP configuration ...")


if __name__ == '__main__':
    EventLoop().run_forever()
