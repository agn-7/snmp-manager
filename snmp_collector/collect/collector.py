import asyncio
import time
import traceback
import struct

from easydict import EasyDict as edict
from pysnmp.hlapi.asyncio import *

from response.response import Response

__author__ = 'aGn'
__copyright__ = "Copyright 2018, Planet Earth"

class SNMPReader(object):
    """SNMP Collector."""
    def __init__(self):
        self.response = Response()
        # self.snmp_engine = SnmpEngine()
        self.context_data = ContextData()

    @staticmethod
    def cast(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError) as exc:
                    print(exc)
        return -8555

    async def read_async_full(
            self,
            loop,
            community_data, udp_transport_target, object_type,
            **kwargs
    ):
        """
        A SNMP collector which is fully asynchronous with asyncio methods.
        :param loop: asyncio loop.
        :param community_data: SNMP community_data.
        :param udp_transport_target: SNMP udp_transport_target.
        :param object_type: SNMP object_type.
        :param kwargs: Below parameters.
        :return:
        """
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        name = kwargs.get('tag_name', 'Default Name')
        module = kwargs.get('name', 'SNMP Device')
        address = kwargs.get('address', 1)
        timeout = kwargs.get('timeout', 1)
        retries = kwargs.get('retries', 3)
        interval = kwargs.get('sleep_time', 3)
        meta = kwargs.get('meta_data', {})
        gain = kwargs.get('gain', 1)
        offset = kwargs.get('offset', 0)
        snmp_engine = kwargs.get('engine', None)

        data = None
        tic = time.time()

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
                print(str_error)
                data = -8555

            elif error_status:
                print('%s at %s' % (
                    error_status.prettyPrint(),
                    error_index and var_binds[int(error_index) - 1][0] or '?'
                )
                      )
                data = -8555

            else:
                for var_bind in var_binds:
                    try:
                        '''var_bind[0] is oid and var_bind[1] is its raw value.'''
                        value = self.cast(var_bind[1])
                        unpacked = struct.unpack('>BBBf', value.encode('latin1'))
                        if unpacked[:3] == (159, 120, 4):
                            '''Checking if data is Opaque or not.'''

                            data = unpacked[-1]
                        else:
                            data = value
                    except AttributeError:
                        data = value
                    except Exception as exc:
                        # print(exc)
                        data = value

                    try:
                        if not isinstance(data, str):
                            '''integer'''
                            data *= gain
                            data += offset
                        else:
                            '''string'''
                            pass

                    except Exception:
                        str_error = f"tag_name: {name} - OID: {oid} - IP: {address} \n " \
                                    f"{traceback.format_exc()}"
                        print(str_error)
                        data = -8555

        except asyncio.CancelledError:
            data = -8555
            raise asyncio.CancelledError()

        except Exception as exc:
            print(exc)
            data = -8555

        finally:
            result = {name: data}
            meta_data = {}

            for met in meta:
                meta_data.update(met)

            self.response.publish(
                module=module,
                meta_data=meta_data,
                **result
            )
            toc = time.time() - tic

            if interval >= (retries * timeout):
                await asyncio.sleep(interval - toc)

            else:
                await asyncio.sleep(interval)
