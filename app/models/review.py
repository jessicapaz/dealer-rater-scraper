from datetime import date
from pydantic import BaseModel, Field


class Review(BaseModel):
    rate: int = Field(int, ge=0, le=50)
    date: date
    comment: str


class ReviewQueryBuilder:
    @staticmethod
    def get_reviews():
        return '#reviews div.review-entry'

    @staticmethod
    def get_date():
        return 'div.review-date > div'

    @staticmethod
    def get_rate():
        return 'div.dealership-rating > div'

    @staticmethod
    def get_comment():
        return 'div.review-wrapper p.review-content'
