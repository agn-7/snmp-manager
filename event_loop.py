import asyncio
import uvloop

from easydict import EasyDict as edict


async def read(config):
    config = edict(config)
    
    try:
        print(config.oid)
    except:
        pass
    finally:
        await asyncio.sleep(config.time)


def event_loop(configs):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # TODO
    loop = asyncio.get_event_loop()

    for conf in configs:
        asyncio.ensure_future(read(conf))

    return loop


async def multiple_tasks(configurations):
    input_coroutines = []
    res = None
    loop = asyncio.get_event_loop()

    for conf in configurations:
        print(1)
        input_coroutines.append(read(conf))
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)

        # asyncio.ensure_future(read(conf))

    if res is not None and loop is not None:
        return res, loop
    else:
        return None, None


def run_once():
    pass


def run_forever():
    while True:
        run_once()


if __name__ == '__main__':
    snmp_configurations = [
        {'time': 2, 'oid': '1.3.6.3.2.4'},
        {'time': 1, 'oid': '1.3.6.3.5.8'},
    ]  # TODO :: DUMMY
    loop = event_loop(snmp_configurations)
    
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()

