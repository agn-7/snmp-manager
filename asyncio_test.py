import asyncio

async def worker(**kwargs):
    oid = kwargs.get('oid', '0.0.0.0.0.0')
    time = kwargs.get('time', 1)

    try:
        # Do stuff.
        print('start: ' + oid)
    except Exception as exc:
        print(exc)
    finally:
        await asyncio.sleep(time)
        print('terminate: ' + oid)


async def worker_with_loop(**kwargs):
    while True:
        oid = kwargs.get('oid', '0.0.0.0.0.0')
        time = kwargs.get('time', 1)

        try:
            # Do stuff.
            print('start: ' + oid)
        except Exception as exc:
            print(exc)
        finally:
            await asyncio.sleep(time)
            print('terminate: ' + oid)


def init_loop(configs):
    loop = asyncio.get_event_loop()

    futures = [
        asyncio.ensure_future(
            worker_with_loop(
                oid=conf['oid'], time=conf['time']
            )
        ) for conf in configs
    ]

    return loop, futures


def run_once(configs):
    print('RUN_ONCE')
    loop, futures = init_loop(configs)
    result = loop.run_until_complete(asyncio.gather(*futures))
    print(result)


def run_forever_built_in(configs):
    print('RUN_FOREVER')
    loop, _ = init_loop(configs)
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()


def run_forever(configs):
    try:
        while True:
            run_once(configs)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    configurations = [
        {'time': 5, 'oid': '1.3.6.3.2.4'},
        {'time': 6, 'oid': '1.3.6.3.5.5'},
        {'time': 1, 'oid': '1.3.6.3.5.6'},
    ]  # TODO :: DUMMY

    # run_once(configurations)
    # run_forever(configurations)
    run_forever_built_in(configurations)
