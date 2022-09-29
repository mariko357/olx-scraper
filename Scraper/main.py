import asyncio
import scraper
from bs4 import BeautifulSoup
soups = asyncio.run(scraper.getMultipleSoupObj(["https://www.olx.ua/d/uk/list/q-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80/" for i in range(10)]))
#print(soups[2].find_all("li"))