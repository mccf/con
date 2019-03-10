
---
- from gevent.monkey import patch_all
patch_all()
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import requests
from gevent import pool
from aiohttp import ClientSession

- yield PEP 255 -- Simple Generators 18-May-2001
- What does the “yield” keyword do? ->
asked:10 years, 4 months ago
viewed:1,964,515 times
link:https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
-Python3.3 版本添加了yield from语法，允许一个generator生成器将其部分操作委派给另一个生成器。其产生的主要动力在于使生成器能够很容易分为多个拥有send和throw方法的子生成器，像一个大函数可以分为多个子函数一样简单。Python的生成器是协程coroutine的一种形式，但它的局限性在于只能向它的直接调用者yield值。这意味着那些包含yield的代码不能如其他代码那样被分离出来放到一个单独的函数中。这也正是yield from要解决的。

- Python3.4版本引入了asyncio，这让Python有了支持异步IO的标准库
- 3.5版本又提供了两个新的关键字async/await，目的是为了更好地标识异步IO，让异步编程看起来更加友好
- 3.6版本更进一步，推出了稳定版的asyncio，从这一系列的更新可以看出，Python社区正迈着坚定且稳重的步伐向异步编程靠近。

- nodejs:用js只需监听事件，编写一个回调函数，则实现高并发。
- Sanic介绍（类似Falsk，快）： https://www.jianshu.com/p/80f4fc313837
- Sanic起源： http://codingpy.com/article/uvloop-blazing-fast-networking-with-python/

- 基准测试通过不同大小的消息，对一个简单的 echo 服务器的性能进行了检测。我们使用了 1、10和 100KB 的包。并发级别设为 10，每个基准测试运行30秒。参见完整的TCP基准测试报告：https://magic.io/blog/uvloop-blazing-fast-python-networking/tcp-bench.html
- aiohttp :Supports both client and server side of HTTP protocol.(可以实现单线程并发IO操作。如果仅用在客户端，发挥的威力不大。如果把asyncio用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+coroutine实现多用户的高并发支持。
asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架。)

### TCP性能对比：

1.asyncio-steams。 使用内置的纯 Python 事件循环的 asyncio 。在这个基准测试里，我们测试了高级别流抽象的性能。我们用 asyncio.create_server() 来创建一个服务器。这个服务器回传一对 (reader, writer) 给客户端的协同程序。

2.tornado。 这个服务器实现了一个简单的 Tornado 协议，可以立即传回它收到的任何数据。

3.curio-steams。Curio 是Python 异步库中的新生儿。和 asyncio-steams 一样，在本次基准测试里我们打算测试 curio 的数据流。我们使用 curio.make_steams() 来创建一对 (reader, writer) ， 提供了一些高级API，比如readline()。

4.twisted。和Tornado类似，这里我们测试了一个最简单的 echo 的协议。

5.curio。 这个基准测试检验 curio 套接字的性能：一个由 sock.recv() 和 sock.sendall() 协同程序组成的紧凑循环。

6.uvloop-streams。 就像第二个(tornado)一样，这里我们测试 asyncio 高级数据流的性能，只不过这次我们使用的是 uvloop 。

7.gevent。我们用 gevent.SteamServer 和一个 gevent 套接字，在紧凑循环中来发送/接收数据。

8.asyncio。看起来原生的 asyncio 也很快！和第 2 个(tornado)和第 4 个(twisted)类似，这里我们测试一个最简的 echo 协议的性能。这个协议是用纯 Python 的 asyncio 实现的。

9.nodejs。我们用 net.createServer API来测试 nodejs v4.2.6 中的数据流性能。

10.uvloop。 这个基准测试中，我们用以 uvloop 为基础的 asyncio 实现一个最简单的 echo 协议(像第2、4、8个一样)，并对该协议的性能进行测试。用 1KB 的信息， uvloop是最快的实现，每秒达到了 105，000 次请求！对于 100KB 的信息来说，uvloop 的传输速度可以做到 2.3 GB/s。

11.Go。使用由net.Conn.Read/Write调用组成的紧凑循环。Golang 的性能和 uvloop 十分相似，对于 10KB 和 100KB 的信息来说性能稍好一些。
### HTTP性能对比
一开始，我们想比较搭建在 asyncio 和 uvloop 之上的 aiohttp 与 nodejs、Go 的性能差别。aiohttp 是用 asyncio 搭建异步 HTTP 服务器最流行的框架。

然而，aiohttp 的性能瓶颈竟然是它的 HTTP 解析器。这个解析器的速度非常慢，导致底层 I/O 库再快也没有用。为了让事情更有趣一点，我们为 http-parser (nodejs 中的 HTTP 解析器，用 C 编写，一开始为 Nginx 开发) 创建了一个 Python 绑定。这个库叫作 httptools ，可在 Github 和 PyPI上找到。

对于 HTTP ，所有的基准测试都使用的 wrk 来生成负载。并发级别设置为 300。每次基准测试的时间为30秒。

HTTP 网络互连性能比较

出人意料的是，有了高性能 HTTP 解析器的帮助，纯 Python 的 asyncio 的速度超过了nodejs，而后者用的也是同一种 HTTP 解析器！

Go在 1KB 的响应上的性能比较快，但是 uvloop+asyncio 的实现在 10/100KB 的表现上明显比较快。对于用 httptools 的 asyncio 和 uvloop 而言，它们的性能非常棒。Go 语言也是一样。

不可否认的是，基于 httptools 的服务器非常的简单，而且比起其他实现方法来，也不包括其他的路由逻辑。然而，这次的基准测试证明了配合一个实现得很有效率的协议，uvloop 可以变得非常之快。

### uvloop

uvloop是用 Cython 写的，其基础是 libuv。

libuv 是 nodejs 使用的一个高性能、多平台的异步 I/O 库。由于 nodejs 使用很广也很流行，使得 libuv 又快又稳定。

uvloop 实现了所有 asyncio 里面的事件循环 API 。高级 Python 对象封装了底层的 libuv 结构体和函数。为了让代码干净、不重复，并保证手动内存管理都和 libuv 的原语生命周期保持一致，uvloop 使用了子类继承的方法。

### 结论
我们可以安全地下结论说，有了 uvloop，我们可以写出每秒每 CPU 核心可以推送上万次请求的 Python 网络互连代码。在一个多核心系统上，用上进程池，也许还可以进一步地提高性能。
在 Python 3.5 中，配合async/awit的力量， uvloop 和 asyncio 使得用 Python 写出高性能的网络互连代码比以前任何时候都简单。
试一试 uvloop(github)，跟我们分享你的结果吧！

