from datetime import date
from pydantic import BaseModel, Field


class Review(BaseModel):
    rate: int = Field(int, ge=0, le=50)
    date: date
    comment: str
