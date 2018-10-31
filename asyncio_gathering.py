"""
Try to remedy the failed_multitask.py
"""

import asyncio


async def test_1(dummy):
    await asyncio.sleep(5)
    res = dummy + 5
    print(res)
    return res

async def test_2(dummy):
    await asyncio.sleep(5)
    res = dummy + 10
    print(res)
    return res

async def multiple_tasks(dummy):
    input_coroutines = [test_1(dummy), test_2(dummy)]
    res = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return res


if __name__ == '__main__':
    dummy = 0
    asyncio.get_event_loop().run_until_complete(multiple_tasks(dummy))

