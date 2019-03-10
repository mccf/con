from gevent.monkey import patch_all
import timeit
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
patch_all()
import requests
from gevent import pool
from aiohttp import ClientSession

workers = 1000


# note:
# sth = 'sth'
# s = [sth] * 10  # return 10 same thing in []


# url = 'https://cn.bing.com/?mkt=zh-CN'
# url = 'https://cn.bing.com/?mkt=zh-CN'
# url = 'https://www.baidu.com/'
url = 'http://127.0.0.1/'
po = pool.Pool(1000)
t = ThreadPoolExecutor(max_workers=100)
p = ProcessPoolExecutor(max_workers=10)


class Req():
    def __init__(self):
        pass

    def get(self, url):
        requests.get(url)


# req = Req()
req = requests


def c_ti(k):
    return req.get(url).text


def ge():
    po.map(c_ti, range(workers))


def sync():
    for i in range(workers):
        c_ti(i)


def th():
    t.map(c_ti, range(workers))
    t.shutdown()


def pr():
    p.map(c_ti, range(workers))
    p.shutdown()


async def test_aio(url):
    async with ClientSession() as session:
        # session = ClientSession()
        async with session.get(url) as r:
            rr = await r.text()
            return rr
            # print(rr)


tasks = [test_aio(url) for x in range(workers)]
loop = asyncio.get_event_loop()


def aio():
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    # timer = timeit.Timer('sync()', 'from __main__ import url,sync')
    # timer = timeit.Timer('ge()', 'from __main__ import ge,url')
    # timer = timeit.Timer('th()', 'from __main__ import th,url')
    # timer = timeit.Timer('pr()', 'from __main__ import pr,url')
    timer = timeit.Timer('aio()', 'from __main__ import aio')
    print(timer.timeit(1))
