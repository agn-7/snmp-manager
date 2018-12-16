import asyncio
import time
import traceback

from easydict import EasyDict as edict
from easysnmp import snmp_get
from pysnmp.hlapi.asyncio import *

from response.response import Response
from utility.logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class SNMPReader(object):
    def __init__(self):
        self.response = Response()
        self.snmp_engine = SnmpEngine()

    async def read_async_full(self, loop, **kwargs):
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        name = kwargs.get('tag_name', 'Default Name')
        module = kwargs.get('name', 'SNMP Device')
        address = kwargs.get('address', 1)
        community = kwargs.get('community', 'public')
        version = kwargs.get('version', 1)
        port = kwargs.get('port', 161)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 3)
        # meta = kwargs.get('meta', {})
        meta = {}  # TODO :: DUMMY

        data = None
        hostname = (address, port)
        tick = time.time()

        try:
            error_indication, error_status, error_index, var_binds = await getCmd(
                self.snmp_engine,
                CommunityData(community),
                UdpTransportTarget(hostname, timeout=timeout, retries=retries),
                ContextData(),
                ObjectType(ObjectIdentity(oid))  # TODO
            )

            if error_indication:
                print(11111)
                print(error_indication)
                data = -8555

            elif error_status:
                print(22222)
                print('%s at %s' % (
                    error_status.prettyPrint(),
                    error_index and var_binds[int(error_index) - 1][0] or '?'
                )
                      )
                data = -8555
            else:
                print(3333)
                for var_bind in var_binds:
                    # print(' = '.join([x.prettyPrint() for x in var_bind]))

                    # for data in var_bind:
                    #     print('data: ', data)

                    print('data: ', var_bind[1])
                    data = float(var_bind[1])

        except Exception as exc:
            print(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    traceback.format_exc()
                )
            )
            logger.captureMessage(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    exc
                )
            )
            data = -8555

        finally:
            result = {name: data}

            self.response.publish(  # TODO
                module=module,
                meta_data=meta,
                **result  # TODO :: handle it
            )
            tack = time.time() - tick

            if interval >= (retries * timeout):
                await asyncio.sleep(interval - tack)

            else:
                await asyncio.sleep(interval)

    async def read_async_semi(self, loop, **kwargs):
        """
        Reading from SNMP with easysnmp lib (sync)
        :param loop: asyncio loop
        :param kwargs: Config stuff
        :return:
        """
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        name = kwargs.get('tag_name', 'Default Name')
        module = kwargs.get('name', 'SNMP Device')
        address = kwargs.get('address', 1)
        community = kwargs.get('community', 'public')
        version = kwargs.get('version', 1)
        port = kwargs.get('port', 161)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 3)
        # meta = kwargs.get('meta', {})
        meta = {}  # TODO :: DUMMY

        data = None
        tick = time.time()

        # async with async_timeout.timeout(timeout * retries):

        try:
            data = float(
                snmp_get(  # TODO :: Check the await at here.
                    oid,
                    hostname=address,
                    community=community,
                    version=version,
                    remote_port=port,
                    timeout=timeout,
                    retries=retries,
                ).value
            )

        except Exception as exc:
            print(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    traceback.format_exc()
                )
            )
            logger.captureMessage(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    exc
                )
            )
            data = -8555

        finally:
            result = {name: float(data)}

            self.response.publish(  # TODO
                module=module,
                meta_data=meta,
                **result  # TODO :: handle it
            )
            tack = time.time() - tick

            if interval >= (retries * timeout):
                # await asyncio.sleep(interval - tack, loop=loop)
                await asyncio.sleep(interval - tack)

            else:
                # await asyncio.sleep(interval, loop=loop)
                await asyncio.sleep(interval)
