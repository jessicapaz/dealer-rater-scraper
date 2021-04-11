from app.scrapers import reviews
import asyncio


def print_top_reviews():
    dealer_name = '''
        McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685'''
    loop = asyncio.get_event_loop()
    top_reviews = reviews.Reviews(dealer_name.strip()).get_top_best_reviews(
        page_range=(1, 6), limit=3)
    top_reviews = loop.run_until_complete(top_reviews)
    for r in top_reviews:
        print(r)


if __name__ == '__main__':
    print_top_reviews()
