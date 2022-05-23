from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from time import sleep
import api.database as database
import api.schemas as schemas
from psycopg2 import IntegrityError 

app = FastAPI()

while True:
    try:
        con, cur = database.initialize_db()
        break
    except:
        for i in range(3, 0,-1):
            print(f"Connection failed ... Retrying in {i}", end = '\r')
            sleep(1)
        print('')

@app.get('/')
def this_page():
    return RedirectResponse("/docs")

#@app.get('/articles/', status_code=status.HTTP_200_OK)
#def get_posts():
#    return {"data":"this is the first article"}

@app.get('/articles/{date}',response_model=schemas.Articles)
def get_articles_by_day(date: str):

    if not schemas.valid_date(date):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = "Invalid date, make sure you follow the format 'YYYY-MM-DD' and using a valid date")

    cur.execute('''SELECT url, title, text, count, date, tags, summary FROM articles WHERE date = %s''',(date,))
    return {f"article{i}":k for i,k in enumerate(cur.fetchall())}

@app.post('/summary/',status_code=status.HTTP_201_CREATED)
def post_summary(summary: schemas.Summary):
    cur.execute('''UPDATE articles SET summary=%s WHERE url = %s RETURNING *''',(summary.summary,summary.url))
    con.commit()
    result = cur.fetchone()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"url {summary.url} not in database")
    return result

@app.post('/')
def get_recommendations(cookie: schemas.Cookie):
    # 
    return {"data":f"{cookie.cookieid}"}

@app.post('/articles/',status_code=status.HTTP_201_CREATED)
async def post_article(article_data: schemas.Article):
    try:
        cur.execute("""INSERT INTO articles(url,title,text,count,tags,summary,date) VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                [article_data.url,article_data.title,article_data.text,article_data.count,article_data.tags,article_data.summary,article_data.date])
        con.commit()
        print('Added article')
    except KeyError as exception:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Item {article_data.url} had no key {repr(exception)}")
    except IntegrityError as exception:
        con.rollback()
        HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail = f'Pipeline raised a {repr(exception)}')
    return {"data":"success"}

@app.post('/users/', status_code=status.HTTP_201_CREATED, response_model= schemas.RatingModel)
def post_rating(rating: schemas.UserRating):
    
    # Get userId associated with cookieId
    cur.execute('''SELECT id FROM users WHERE cookie_id = %s''',(rating.cookieid,))
    id: dict = cur.fetchone()
    if id == None:
        cur.execute('''INSERT INTO users (cookie_id) VALUES (%s) RETURNING id''',(rating.cookieid,))
        id: dict = cur.fetchone()
    id: str = id['id']

    # Insert value, updates rating if user rated the URL before, returns None if URL doesn't exist in database
    cur.execute('''WITH data AS (SELECT %s AS id,sk,%s AS rating, url FROM articles WHERE url = %s)
                    INSERT INTO users_ratings SELECT id,sk,rating from data
                    ON CONFLICT (user_id,article_id) DO UPDATE SET rating = %s
                    RETURNING (SELECT url FROM data), rating ;'''
                    ,(id,rating.rating,rating.url,rating.rating)) 

    con.commit()

    inserted_data = cur.fetchone()
    if inserted_data == None:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = "Invalid url")
    return inserted_data

#SELECT u.cookie_id, a.url, r.rating
#FROM users_ratings r
#INNER JOIN users u ON user_id = u.id
#INNER JOIN articles a ON article_id = a.sk;