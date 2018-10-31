import asyncio

async def read(config):
    try:
        pass
    except:
        pass
    finally:
        await asyncio.sleep(config.interval)


async def event_loop():
    pass


async def multiple_tasks(configurations):
    input_coroutines = []
    res = None
    loop = asyncio.get_event_loop()

    for conf in configurations:
        input_coroutines.append(read(conf))
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)

        asyncio.ensure_future(read(conf))

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

    try:
        snmp_configurations = [
            {'time': 2, 'oid': '1.3.6.3.2.4'},
            {'time': 1, 'oid': '1.3.6.3.5.8'},
        ]  # TODO :: DUMMY
        tasks, loop = multiple_tasks(snmp_configurations)

        while True:
            loop.run_until_complete(tasks)

        '''Or this approach instead of above while.'''
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()

