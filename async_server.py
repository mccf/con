import datetime
import asyncio

from aiohttp import web


async def index(request):
    print(datetime.datetime.now())
    await asyncio.sleep(0.5)
    return web.Response(body='Index')


async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    # srv = await loop.create_server(app.make_handler(), '127.0.0.1', 800)
    runner = web.AppRunner(app)
    await runner.setup()
    srv = await loop.create_server(runner.server, '127.0.0.1', 80)
    print('Server started at http://127.0.0.1...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
