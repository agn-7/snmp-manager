import asyncio
import uvloop


async def read(**kwargs):
    oid = kwargs.get('oid', '0.0.0.0.0.0')
    time = kwargs.get('time', 1)

    try:
        print('start: ' + oid)
    except Exception as exc:
        print(exc)
    finally:
        await asyncio.sleep(time)
        print('terminate: ' + oid)


def event_loop(configs):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # TODO  :: uvloop.
    loop = asyncio.get_event_loop()

    for conf in configs:
        asyncio.ensure_future(read(oid=conf['oid'], time=conf['time']))

    return loop


if __name__ == '__main__':
    snmp_configurations = [
        {'time': 5, 'oid': '1.3.6.3.2.4'},
        {'time': 6, 'oid': '1.3.6.3.5.8'},
    ]  # TODO :: DUMMY
    loop = event_loop(snmp_configurations)

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()

