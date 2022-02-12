import asyncio
import async_timeout
import time
import traceback
import sys
import gc
import argparse
import os

from pysnmp.error import PySnmpError
from pysnmp.hlapi.asyncio import *
from colored_print import ColoredPrint

try:
    from snmp_collector.read_conf.read_configuration import get_config
    from snmp_collector.collect.collector import SNMPReader
    from snmp_collector.utility.utility import Utility
except:
    from read_conf.read_configuration import get_config
    from collect.collector import SNMPReader
    from utility.utility import Utility

log = ColoredPrint()

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"


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
        community = kwargs.get('community', 'public')
        address = kwargs.get('address', '127.0.0.1')
        port = kwargs.get('port', 161)
        hostname = (address, port)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        version = kwargs.get('version', 1)

        community_data = CommunityData(community, mpModel=version-1)
        udp_transport_target = UdpTransportTarget(hostname, timeout=timeout, retries=retries)
        object_type = ObjectType(ObjectIdentity(oid))
        while True:
            try:
                # async with async_timeout.timeout(total_timeout) as cm:
                await self.snmp_reader.read_async_full(
                    loop,
                    community_data, udp_transport_target, object_type,
                    **kwargs
                )

            # except asyncio.TimeoutError as exc:
            #     print(cm.expired, exc)
            #     pass

            except KeyboardInterrupt:
                loop.close()

    def run_once(self):
        """Run once method in asyncio tech."""

        loop = asyncio.get_event_loop()
        configs = get_config()

        if configs:
            for conf in configs:
                hostname = (conf['address'], conf['port'])
                community_data = CommunityData(
                    conf['community'],
                    mpModel=conf['version']-1
                )
                udp_transport_target = UdpTransportTarget(
                    hostname,
                    timeout=conf['timeout'], retries=conf['retries']
                )
                object_type = ObjectType(ObjectIdentity(conf['oid']))
                futures = [asyncio.ensure_future(
                    self.snmp_reader.read_async_full(
                        loop, community_data, udp_transport_target, object_type,
                        **conf)
                )]

            result = loop.run_until_complete(asyncio.gather(*futures))
            print(result)
            return True

        else:
            return False

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
    def stop_auth(auth):
        """Stop ZAP"""
        try:
            auth.stop
        except Exception as exc:
            print(exc)

    @staticmethod
    def destroy_snmp_engines(engine):
        """
        Destroy SNMP-Engine instance.
        :param engine:
        :return:
        """
        try:
            # engine.transportDispatcher.closeDispatcher()
            engine.unregisterTransportDispatcher()

        except PySnmpError as snmp_exc:
            print(snmp_exc)

        except Exception as exc:
            print(exc)

    def termination(self, configs, futures):
        """
        Destroy some expensive instances: Stop ZAP, Destroy SNMP-Engines, Destroy Zombie
        coroutine Asyncio tasks and clear other memory usage by Python GC.
        :param configs: SNMP configuration
        :param futures: Asyncio coroutine tasks.
        :return:
        """
        for f in futures:
            f.cancel()

        for conf in configs:
            self.destroy_snmp_engines(conf['engine'])

            for srv in conf['servers']:
                try:
                    self.stop_auth(srv['auth'])
                except Exception as exc:
                    print(exc)

        gc.collect()  # TODO

    def run_forever(self):
        """Forever event-loop with the loop re-starter ability in asyncio tech."""
        
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
                        print(info_)

                try:
                    '''Run'''
                    loop.run_forever()

                    '''Termination'''
                    self.termination(configs, futures)

                except KeyboardInterrupt:
                    print("The process was killed.")
                    loop.close()
                    sys.exit(0)

                except asyncio.CancelledError:
                    print('Tasks has been canceled.')
                    loop.close()

                except Exception:
                    print(traceback.format_exc())

            else:
                time.sleep(5)
                log.info("Waiting for SNMP configuration ...")


def run():
    print('SNMP Begins')
    parser = argparse.ArgumentParser(description='Simple SNMP Collector.')

    try:
        parser.add_argument('--config', type=str, help='SNMP Configuration JSON path.')
        args = parser.parse_args()
        if args.config is not None:
            os.environ["CONFIG_PATH"] = args.config

        EventLoop().run_forever()

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run()
