import pytest
import datetime
from unittest.mock import patch

from app.scrapers.reviews import Reviews
from app.models.review import Review


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_get_reviews_with_success(
        mock_request, mock_review_page
    ):
    mock_request = mock_request.return_value.__aenter__.return_value
    mock_request.text.return_value = mock_review_page
    dealer_name = 'McKaig Chevrolet Buick A Dealer'

    expected = [
        Review(rate=48, date=datetime.date(2021, 1, 23),
               comment="Great customer service"),
        Review(rate=50, date=datetime.date(2021, 1, 18),
               comment="Great guy worked hard to get us pur deal."),
        Review(rate=50, date=datetime.date(2021, 1, 22),
               comment="Excellent service!"),
        Review(rate=50, date=datetime.date(2021, 1, 22),
               comment="Really easy to deal with."),
        Review(rate=50, date=datetime.date(2021, 1, 20),
               comment="David is fantastic!"),
        Review(rate=50, date=datetime.date(2021, 1, 20),
               comment="I needed a larger vehicle for my family."),
        Review(rate=50, date=datetime.date(2021, 1, 19),
               comment="Good"),
        Review(rate=50, date=datetime.date(2021, 1, 23),
               comment="Mckaig is the one"),
        Review(rate=50, date=datetime.date(2021, 1, 18),
               comment="I was very impressed"),
        Review(rate=50, date=datetime.date(2021, 1, 17),
               comment="The service department is second to none")
    ]

    actual = await Reviews(dealer_name).get_by_pages(page_range=(1, 2))

    assert actual == expected


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_get_top_reviews_with_success(
        mock_request, mock_review_page
    ):
    mock_request = mock_request.return_value.__aenter__.return_value
    mock_request.text.return_value = mock_review_page
    dealer_name = 'McKaig Chevrolet Buick A Dealer'

    expected = [
        Review(rate=50, date=datetime.date(
            2021, 1, 23), comment="Mckaig is the one"),
        Review(rate=50, date=datetime.date(2021, 1, 22),
               comment="Excellent service!"),
        Review(rate=50, date=datetime.date(2021, 1, 22),
               comment="Really easy to deal with.")
    ]

    actual = await Reviews(dealer_name).get_top_best_reviews((1, 2), 3)

    assert actual == expected
