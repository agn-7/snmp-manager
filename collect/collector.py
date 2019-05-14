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
        # self.snmp_engine = SnmpEngine()
        self.context_data = ContextData()

    async def read_async_full(
            self,
            loop,
            community_data, udp_transport_target, object_type,
            **kwargs
    ):
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
        version = kwargs.get('version', 1)
        port = kwargs.get('port', 161)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 3)
        servers = kwargs.get('servers', [{'name': 'default', 'ip': '127.0.0.1', 'port': 9001}])
        pipeline_ip = kwargs.get('pipeline_ip', '127.0.0.1')
        pipeline_port = kwargs.get('pipeline_port', 9001)
        meta = kwargs.get('meta_data', {})
        gain = kwargs.get('gain', 1)
        offset = kwargs.get('offset', 0)
        snmp_engine = kwargs.get('engine', None)

        servers_obj = [edict(server) for server in servers]

        if pipeline_ip != '127.0.0.1':
            for server in servers_obj:
                server.ip = pipeline_ip
                server.port = pipeline_port

        data = None
        tick = time.time()

        try:
            error_indication, error_status, error_index, var_binds = await getCmd(
                snmp_engine,
                community_data,
                udp_transport_target,
                self.context_data,
                object_type
            )

            if error_indication:
                str_error = f"tag_name: {name} - OID: {oid} - IP: {address} \n " \
                            f"{error_indication}"
                # logger.captureMessage(str_error)  # TODO
                data = -8555

            elif error_status:
                # logger.captureMessage(
                #     f"{error_status.prettyPrint()} at "
                #     f"{error_index and var_binds[int(error_index) - 1][0] or '?'}"
                #
                # )  # TODO
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
                        data *= gain
                        data += offset

                    except ValueError:
                        str_error = f"tag_name: {name} - OID: {oid} - IP: {address} \n " \
                                    f"{traceback.format_exc()}"
                        # logger.captureMessage(str_error)  # TODO
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
            meta_data = {}
            for met in meta:
                meta_data.update(met)

            self.response.publish(
                module=module,
                meta_data=meta_data,
                servers=servers_obj,
                **result
            )
            tack = time.time() - tick

            if interval >= (retries * timeout):
                await asyncio.sleep(interval - tack)

            else:
                await asyncio.sleep(interval)

