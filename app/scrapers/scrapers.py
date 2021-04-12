import aiohttp
from bs4 import BeautifulSoup
from app.models.scraper import HTMLTag


class HTMLScraper:
    @staticmethod
    def parse_page(page):
        return BeautifulSoup(page, 'html.parser')

    @staticmethod
    async def request(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    @staticmethod
    def get_container_tag(page, query):
        return page.select(query)

    @staticmethod
    def get_first(page, query):
        html_block = page.select(query)[0]
        return HTMLTag(classes=html_block['class'], content=html_block.text)
