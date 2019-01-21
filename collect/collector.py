import asyncio
import time
import traceback

from easydict import EasyDict as edict
from pysnmp.hlapi.asyncio import *

from response.response import Response
from utility.logger import Logging

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

logger = Logging().sentry_logger()


class SNMPReader(object):
    """SNMP Collector."""
    def __init__(self):
        self.response = Response()
        self.snmp_engine = SnmpEngine()

    async def read_async_full(self, loop, **kwargs):
        """
        A SNMP collector which is fully asynchronous with asyncio methods.
        :param loop: asyncio loop.
        :param kwargs: Below parameters.
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
        servers = kwargs.get('servers', [{'name': 'default', 'ip': '127.0.0.1', 'port': 9001}])
        pipeline_ip = kwargs.get('pipeline_ip', '127.0.0.1')
        pipeline_port = kwargs.get('pipeline_port', 9001)
        meta = kwargs.get('meta', {})

        servers_obj = []
        for server in servers:
            servers_obj.append(edict(server))

        if pipeline_ip is not '127.0.0.1':
            for server in servers_obj:
                server.ip = pipeline_ip
                server.port = pipeline_port

        data = None
        hostname = (address, port)
        tick = time.time()

        try:
            error_indication, error_status, error_index, var_binds = await getCmd(
                self.snmp_engine,
                CommunityData(community),
                UdpTransportTarget(hostname, timeout=timeout, retries=retries),
                ContextData(),
                ObjectType(ObjectIdentity(oid))  # TODO :: Add SNMP version.
            )

            if error_indication:
                logger.captureMessage(error_indication)
                data = -8555

            elif error_status:
                logger.captureMessage(
                    f"{error_status.prettyPrint()} at "
                    f"{error_index and var_binds[int(error_index) - 1][0] or '?'}"

                )
                print('%s at %s' % (
                    error_status.prettyPrint(),
                    error_index and var_binds[int(error_index) - 1][0] or '?'
                )
                      )
                data = -8555

            else:
                for var_bind in var_binds:
                    try:
                        data = float(var_bind[1])
                    except ValueError:
                        str_error = f"tag_name: {name} - OID: {oid} - IP: {address} \n " \
                                    f"{traceback.format_exc()} - msg: {var_bind[1]}"
                        logger.captureMessage(str_error)
                        data = -8555

        except asyncio.CancelledError:
            data = -8555
            raise asyncio.CancelledError()

        except Exception:
            logger.captureMessage(
                "IP : {} - NAME : {} - OID : {} >> {}".format(
                    address,
                    name,
                    oid,
                    traceback.format_exc()
                )
            )
            data = -8555

        finally:
            result = {name: data}

            self.response.publish(
                module=module,
                meta_data=meta,
                servers=servers_obj,
                **result
            )
            tack = time.time() - tick

            if interval >= (retries * timeout):
                await asyncio.sleep(interval - tack)

            else:
                await asyncio.sleep(interval)

