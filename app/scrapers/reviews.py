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
            published_date = self._get_published_date(
                review, ReviewQueryBuilder.get_published_date())
            rating = self._get_rating(review, ReviewQueryBuilder.get_rating())
            comment = HTMLScraper.get_first(
                review, ReviewQueryBuilder.get_comment()).content
            author = self._get_author(review, ReviewQueryBuilder.get_author())

            review = Review(
                published_date=published_date,
                rating=rating, comment=comment,
                author=author
            )
            parsed_reviews.append(review)
        return parsed_reviews

    def _get_published_date(self, review, published_date_query):
        published_date = HTMLScraper.get_first(
            review, published_date_query).content
        return datetime.strptime(published_date, '%B %d, %Y')

    def _get_rating(self, review, rating_query):
        rating = HTMLScraper.get_first(review, rating_query)
        regex_pattern = '.*rating-([0-9]+)'
        rating_number = int(re.search(regex_pattern, ' '.join(
            rating.classes)).group(1))
        return round(rating_number / 10, 1)

    def _get_author(self, review, author_query):
        author = HTMLScraper.get_first(review, author_query).content
        return author.replace('-', '').strip()

    async def get_top_best_reviews(self, page_range, limit):
        all_reviews = await self.get_by_pages(page_range)
        sorted_reviews = sorted(
            all_reviews,
            key=lambda r: (r.rating, r.published_date),
            reverse=True
        )
        return sorted_reviews[:limit]
