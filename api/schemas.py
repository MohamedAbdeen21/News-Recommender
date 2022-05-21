from pydantic import BaseModel,create_model, validator
from datetime import datetime, date
from typing import Dict, Optional, Type

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

class Cookie(BaseModel):
    cookieid: str

class UserRating(RatingModel, Cookie):
    pass

class Summary(BaseModel):
    url: str
    summary: str

class Article(Summary):
    title: str
    text: str
    count: int
    summary: Optional[str]
    date: date

class Articles(BaseModel):
    __root__: Dict[str,Article]
