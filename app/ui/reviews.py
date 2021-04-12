import argparse
from tabulate import tabulate

from app.scrapers.reviews import Reviews


class ReviewsUI:
    async def print_top_reviews(self):
        reviews = await self.top_reviews
        formated_data = tabulate(
            [[r.date, r.rate, r.comment] for r in reviews],
            headers=['Date', 'Rate', 'Comment']
        )
        print(formated_data)

    @property
    async def top_reviews(self):
        reviews = Reviews(self._args.dealer)
        page_range = (self._args.page_start, self._args.page_end)
        limit = self._args.limit
        return await reviews.get_top_best_reviews(page_range, limit)

    @property
    def _args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--limit', type=int, required=True)
        arg_parser.add_argument('--dealer', type=str, required=True)
        arg_parser.add_argument(
            '--page_start', type=int, required=True)
        arg_parser.add_argument(
            '--page_end', type=int, required=True)
        args = arg_parser.parse_args()
        return args
