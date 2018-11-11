import asyncio
import async_timeout
import time
import traceback

from easydict import EasyDict as edict
from easysnmp import snmp_get

from response import Response
from logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class SNMPReader(object):
    def __init__(self):
        self.response = Response()

    async def read(self, loop, **kwargs):
        """

        :param loop:
        :param kwargs:
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

            data = None

        finally:
            result = {name: data}

            self.response.publish(
                module=module,
                meta_data=meta,
                server_ip='172.17.0.1',  # TODO :: DUMMY
                pipeline_ip='172.17.0.1',  # TODO :: DUMMY
                pipeline_port='9001',  # TODO :: DUMMY
                **result  # TODO :: handle it
            )
            tack = time.time() - tick

            if interval >= (retries * timeout):
                await asyncio.sleep(interval - tack, loop=loop)

            else:
                await asyncio.sleep(interval, loop=loop)
