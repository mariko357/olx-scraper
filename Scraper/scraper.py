import asyncio
import aiohttp
from multiprocessing import Process, Queue
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

def getSoupObjThreaded(outq, page):
    soup = BeautifulSoup(page, "html.parser")
    outq.put([soup])

async def getMultipleSoupObj(urls):
    pages = []
    pages = await asyncio.gather(*(getPageContents(i) for i in urls))
    soups = Queue()
    rsoups = []
    workers = []

    for i in pages:
        worker = Process(target=getSoupObjThreaded, args=(soups, i))
        workers.append(worker)
        worker.start()

    for i in workers:
        temp = soups.get()
        rsoups.append(temp)

    for i in workers:
        i.join()
    
    return rsoups
