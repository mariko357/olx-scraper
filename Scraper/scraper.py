import asyncio
import aiohttp
import multiprocessing
from bs4 import BeautifulSoup
import sys


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

def getSoupObjThreaded(page):
    soup = BeautifulSoup(page, "html.parser")
    return soup


async def getMultipleSoupObj(urls):
    pages = []
    pages = await asyncio.gather(*(getPageContents(i) for i in urls))
    sys.setrecursionlimit(1000000)
    out = []
    pool = multiprocessing.Pool()
    out = pool.map(getSoupObjThreaded, pages)
    return out
