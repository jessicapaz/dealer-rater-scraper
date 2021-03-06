import pytest
import os


@pytest.fixture
def mock_review_page():
    with open(f'{os.getcwd()}/tests/unit/fixtures/page_review.html') as page:
        return page.read()
