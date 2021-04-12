import argparse
import pytest
from unittest.mock import patch

from app.ui.reviews import ReviewsUI


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
@patch('argparse.ArgumentParser.parse_args')
async def test_get_top_reviews_with_success(
        mock_args, mock_request, mock_review_page, capfd
    ):
    mock_request = mock_request.return_value.__aenter__.return_value
    mock_request.text.return_value = mock_review_page
    mock_args.return_value = argparse.Namespace(
        dealer='McKaig Chevrolet Buick A Dealer',
        page_range=[1, 2],
        limit=2
    )

    expected = '''
    Date          Rate  Comment
    ----------  ------  ------------------
    2021-01-23      50  Mckaig is the one
    2021-01-22      50  Excellent service!
    '''

    await ReviewsUI().print_top_reviews()

    actual, err = capfd.readouterr()

    assert actual.split() == expected.split()
