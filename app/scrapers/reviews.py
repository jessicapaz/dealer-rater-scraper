import asyncio
import re

from app import config
from app.models.review import Review
from datetime import datetime
from app.scrapers.scraper import Scraper


class Reviews:
    def __init__(self, dealer_name):
        self._base_url = f'{config.DEALER_RATER["url"]}/dealer/{dealer_name}'

    async def _get_review_pages(self, page_range):
        return await asyncio.gather(
            *[Scraper.request(f'{self._base_url}/page{i}')
              for i in range(*page_range)]
        )

    def _parse_reviews_page(self, page):
        parsed_reviews = []
        container_tag = Scraper.get_container_tag(page, 'reviews')
        reviews = container_tag.find_all('div', 'review-entry')
        for review in reviews:
            date = Scraper.get_first_child(
                review, 'div', 'review-date', 'div').text
            date_formated = datetime.strptime(date, '%B %d, %Y')
            rate = self._get_rate(review)
            comment_div = Scraper.get(review, 'div', 'review-wrapper')
            comment = Scraper.get(comment_div, 'p', 'review-content').text
            parsed_reviews.append(
                Review(date=date_formated, rate=rate, comment=comment))
        return parsed_reviews

    def _get_rate(self, review):
        rate_div = Scraper.get_first_child(
            review, 'div', 'dealership-rating', 'div')
        regex_pattern = '.*rating-([0-9]+)'
        rate = int(re.search(regex_pattern, ' '.join(
            rate_div['class'])).group(1))
        return rate

    async def get_by_pages(self, page_range):
        pages = await self._get_review_pages(page_range)
        reviews = []
        for page in pages:
            reviews += self._parse_reviews_page(page)
        return reviews

    async def get_top_best_reviews(self, page_range, limit):
        all_reviews = await self.get_by_pages(page_range)
        sorted_reviews = sorted(
            all_reviews, key=lambda r: (r.rate, r.date), reverse=True)
        return sorted_reviews[:limit]
