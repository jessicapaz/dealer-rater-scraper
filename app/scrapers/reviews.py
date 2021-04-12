import asyncio
import re
from datetime import datetime

from app import config
from app.models.review import Review
from app.models.review import ReviewQueryBuilder
from app.scrapers.scrapers import HTMLScraper


class Reviews:
    def __init__(self, dealer_name):
        self._base_url = f'{config.DEALER_RATER["url"]}/dealer/{dealer_name}'

    async def get_by_pages(self, page_range):
        pages = await self._get_review_pages(page_range)
        reviews = []
        for page in pages:
            reviews += self._parse_reviews_page(page)
        return reviews

    async def _get_review_pages(self, page_range):
        start, end = page_range
        return await asyncio.gather(
            *[HTMLScraper.request(f'{self._base_url}/page{i}')
              for i in range(start, end+1)]
        )

    def _parse_reviews_page(self, page):
        page = HTMLScraper.parse_page(page)
        reviews = HTMLScraper.get_container_tag(
            page, ReviewQueryBuilder.get_reviews())

        parsed_reviews = []
        for review in reviews:
            date = self._get_date(review, ReviewQueryBuilder.get_date())
            rate = self._get_rate(review, ReviewQueryBuilder.get_rate())
            comment = HTMLScraper.get_first(
                review, ReviewQueryBuilder.get_comment()).content
            parsed_reviews.append(
                Review(date=date, rate=rate, comment=comment))
        return parsed_reviews

    def _get_date(self, review, date_query):
        date = HTMLScraper.get_first(
            review, ReviewQueryBuilder.get_date()).content
        return datetime.strptime(date, '%B %d, %Y')

    def _get_rate(self, review, rate_query):
        rate = HTMLScraper.get_first(review, rate_query)
        regex_pattern = '.*rating-([0-9]+)'
        return int(re.search(regex_pattern, ' '.join(
            rate.classes)).group(1))

    async def get_top_best_reviews(self, page_range, limit):
        all_reviews = await self.get_by_pages(page_range)
        sorted_reviews = sorted(
            all_reviews, key=lambda r: (r.rate, r.date), reverse=True)
        return sorted_reviews[:limit]
