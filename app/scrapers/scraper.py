import aiohttp
from bs4 import BeautifulSoup


class Scraper:
    @staticmethod
    async def request(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    @staticmethod
    def get_container_tag(page, container_tag_id):
        soup = BeautifulSoup(page, 'html.parser')
        return soup.find(id=container_tag_id)

    @staticmethod
    def get(page, tag, class_name):
        return page.find(tag, class_=class_name)

    @staticmethod
    def get_all(page, tag, class_name):
        return page.find_all(tag, class_=class_name)

    @staticmethod
    def get_first_child(
            page, parent_tag_name, parent_class_name, child_tag_name):
        query = f'{parent_tag_name}.{parent_class_name} > {child_tag_name}'
        return page.select(query)[0]
