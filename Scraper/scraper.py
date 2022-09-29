import asyncio
import aiohttp
import multiprocessing
from bs4 import BeautifulSoup


async def getPageContents(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            page = await resp.read()
    return page

async def getSoupObj(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            page = await resp.read()
    soup = BeautifulSoup(page, "html.parser")
    return soup

def getSoupObjThreaded(page, send_end):
    soup = BeautifulSoup(page, "html.parser")
    print(soup)
    send_end.send(2)

async def getMultipleSoupObj(urls):
    pages = []
    pages = await asyncio.gather(*(getPageContents(i) for i in urls))

    workers = []
    pipes = []
    for i in pages:
        recv_end, send_end = multiprocessing.Pipe(False)
        worker = multiprocessing.Process(target=getSoupObjThreaded, args=(i, send_end))
        workers.append(worker)
        pipes.append(recv_end)
        worker.start()

    for i in workers:
        i.join()
    
    ret = [x.recv() for x in pipes]

    return ret
