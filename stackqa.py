import asyncio
import uvloop
import async_timeout
import time
from datetime import datetime


async def doing(loop, i):
    print('Hi', i,  datetime.now().strftime('%H:%M:%S'))
    await asyncio.sleep(i+3)
    print('Terminate', i,  datetime.now().strftime('%H:%M:%S'))

async def doing_once(loop, i):
    try:
        with async_timeout.timeout(8, loop=loop) as cm:
            await asyncio.sleep(7, loop=loop)
            print("I'm here.", i)

    except asyncio.TimeoutError as exc:
        print('Timeout', i)

async def doing_forever(loop, i):
    while True:
        try:
            async with async_timeout.timeout(5) as cm:
                # print("Hi")
                # await asyncio.sleep(7, loop=loop)
                await doing(loop, i)

        except asyncio.TimeoutError as exc:
            # print(cm.expired, exc)
            print('Timeout', i)

def init_loop(iteration, forever=True):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    '''Set the uvloop event loop policy.'''

    loop = asyncio.get_event_loop()

    if not forever:
        '''Run once.'''
        futures = [asyncio.ensure_future(doing_once(loop, i))
                   for i in range(iteration)]

    else:
        '''Run forever.'''
        futures = [asyncio.ensure_future(doing_forever(loop, i))
                   for i in range(iteration)]

    return loop, futures

def run_once():
    print('RUN_ONCE')
    loop, futures = init_loop(iteration=5, forever=False)
    result = loop.run_until_complete(asyncio.gather(*futures))
    print(result)

def run_forever():
    print('RUN_FOREVER')
    loop, _ = init_loop(iteration=5, forever=True)

    try:
        loop.run_forever()

    except KeyboardInterrupt:
        pass

    finally:
        print("Closing Loop")
        loop.close()

if __name__ == '__main__':  # TODO :: Test.
    # run_once()
    run_forever()
