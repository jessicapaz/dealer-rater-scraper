import asyncio
from app.ui.reviews import ReviewsUI


if __name__ == '__main__':
    asyncio.run(ReviewsUI().print_top_reviews())
