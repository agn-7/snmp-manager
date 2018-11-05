import asyncio

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

    async def read(self, **kwargs):
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        name = kwargs.get('tag_name', 'Default Name')
        module = kwargs.get('name', 'SNMP Device')
        address = kwargs.get('address', 1)
        community = kwargs.get('community', 'public')
        version = kwargs.get('version', 1)
        port = kwargs.get('port', 161)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 1)

        # meta = kwargs.get('meta', {})

        meta = {}  # TODO :: DUMMY

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

            result = {name: data}

            self.response.publish(
                module=module,
                meta_data=meta,
                server_ip='172.17.0.1',  # TODO :: DUMMY
                pipeline_ip='172.17.0.1',  # TODO :: DUMMY
                pipeline_port='9001',  # TODO :: DUMMY
                **result
            )

        except Exception as exc:
            print(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    exc
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

            result = None

            self.response.publish(
                module=module,
                meta_data=meta,
                server_ip='172.17.0.1',  # TODO :: DUMMY
                pipeline_ip='172.17.0.1',  # TODO :: DUMMY
                pipeline_port='9001',  # TODO :: DUMMY
                **result  # TODO :: handle it
            )

        finally:
            await asyncio.sleep(interval)

