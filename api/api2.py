from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, validator
from datetime import datetime
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from time import sleep

app = FastAPI()

while True:
    try:
        con = pg.connect("host=pgdatabase dbname=newsscraper port=5432 user=root password=root", cursor_factory=RealDictCursor)
        cur = con.cursor()
        break
    except:
        for i in range(3,-1,-1):
            print(f"Connection failed ... Retrying in {i}", end = '\r')
            sleep(1)
        continue


def valid_date(date: str) -> bool:
    FORMAT = "%Y-%m-%d"
    try:
        datetime.strptime(date,FORMAT)
        return True
    except ValueError:
        return False

class UserRating(BaseModel):
    cookieID: str
    url: str
    rating: Optional[int] = 0

    @validator('rating',pre=True)
    def right_values(cls, value):
        '''
        Pre argument runs before any other check.
        This is to make sure that the value is an int.
        This is to prevent 'Optional' from truncating floats.
        '''
        assert value in [0,1,2,3,4,5]
        return value
    
class Summary(BaseModel):
    url: str
    summary: str


@app.get('/')
def root():
    return RedirectResponse("/docs")
    

@app.get('/articles/', status_code=status.HTTP_200_OK)
def get_posts():
    return {"data":"this is the first article"}

@app.post('/users/', status_code=status.HTTP_201_CREATED)
def post_user(read_data: UserRating):
    #if read_data.cookieID in DB:
    #   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
    #                        detail = "cookieID is not unique.")
    return read_data

@app.get('/articles/{date}')
def get_article(date: str):
    if not valid_date(date):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = "Invalid date, make sure you follow the format 'YYYY-MM-DD' and using a valid date")
    cur.execute('''SELECT url, title, text, count FROM articles WHERE date = %s''',(date,))
    return {f"article {i}":k for i,k in enumerate(cur.fetchall())}

@app.post('/articles/',status_code=status.HTTP_201_CREATED)
def post_summary(summary: Summary):
    cur.execute('''UPDATE articles SET summary=%s WHERE url = %s RETURNING *''',(summary.summary,summary.url))
    con.commit()
    result = cur.fetchone()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"url {summary.url} not in database")
    return result