from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional

def valid_date(date: str) -> bool:
    FORMAT = "%Y-%m-%d"
    try:
        datetime.strptime(date,FORMAT)
        return True
    except ValueError:
        return False

class RatingModel(BaseModel):
    url: str
    rating: int

    @validator('rating',pre=True)
    def right_values(cls, value: int) -> int:
        '''
        Pre argument runs before any other check.
        This is to make sure that the value is an int.
        This is to prevent 'Optional' from truncating floats.
        '''
        assert value in [0,1,2,3,4,5]
        return value

class UserRating(RatingModel):
    cookieid: str

class Summary(BaseModel):
    url: str
    summary: str

class Article(Summary):
    title: str
    text: str
    count: int
    summary: Optional[str]
    tags: str
    date: str

class ArticlesResponse(Article):
    date: date
    summary: str

class Articles(BaseModel):
    __root__ : List[ArticlesResponse]

class Recommendation(BaseModel):
    cookieid: str
    url: str

class Success(BaseModel):
    success: str