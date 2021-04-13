from datetime import date
from pydantic import BaseModel, Field


class Review(BaseModel):
    rating: int = Field(int, ge=0, le=5)
    published_date: date
    comment: str
    author: str


class ReviewQueryBuilder:
    @staticmethod
    def get_reviews():
        return '#reviews div.review-entry'

    @staticmethod
    def get_published_date():
        return 'div.review-date > div'

    @staticmethod
    def get_rating():
        return 'div.dealership-rating > div'

    @staticmethod
    def get_comment():
        return 'div.review-wrapper p.review-content'

    @staticmethod
    def get_author():
        return 'div.review-wrapper span'
