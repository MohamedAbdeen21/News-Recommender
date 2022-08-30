from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
import api.database as database
import api.schemas as schemas
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extensions import AsIs
from time import sleep

app = FastAPI()
origins = ["*"] # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attempt DB connection and creating the tables
while True:
    try:
        con, cur = database.initialize_db()
        break
    except Exception as e:
        for i in range(3, 0,-1):
            print(f"Connection failed ... Retrying in {i} {repr(e)}", end = '\r')
            sleep(1)
        print('')

@app.get('/api/')
def this_page():
    return RedirectResponse("/docs")

@app.get('/articles/{date}',response_model=schemas.Articles)
def get_articles_by_day(date: str):

    if not schemas.valid_date(date):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = "Invalid date, make sure you follow the format 'YYYY-MM-DD' and using a valid date")

    cur.execute('''SELECT url, title, text, count, date, tags, summary FROM articles WHERE date = %s''',(date,))
    data = cur.fetchall()
    if data == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data

@app.get('/{cookieid}', status_code=status.HTTP_200_OK, response_model=schemas.Articles)
def get_recommendations(cookieid: str):
    # First time user
    try:
        cur.execute('''WITH group_data AS (SELECT group_id AS id FROM users WHERE cookie_id = %s)
                        SELECT url, title, text, count, a.date, summary, tags
                        FROM articles AS a
                        JOIN recommendations AS r 
                        ON r.article_id = a.sk
                        WHERE r.group_id = (SELECT id FROM group_data) ''',
                        (cookieid,))
        return cur.fetchall()
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{repr(e)}")

@app.get('/users_history/',status_code=status.HTTP_200_OK, response_model=schemas.History)
def get_users_history():
    try:
        cur.execute('''SELECT u.cookie_id, a.text, a.url
                        FROM users_ratings AS r
                        INNER JOIN articles AS a
                        ON a.sk = r.article_id
                        INNER JOIN users AS u 
                        ON u.id = r.user_id
                    ''')
        return cur.fetchall()
    except Exception as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{repr(exception)}")

@app.get('/all/',status_code=status.HTTP_200_OK, response_model = schemas.Articles)
def get_all_articles():
    cur.execute('''
                SELECT * FROM articles
                ''')
    return cur.fetchall()

@app.patch('/update_group/{cookie_id}/{group_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.Success)
def update_user_group(cookie_id: str, group_id: str):
    cur.execute('''UPDATE users SET group_id = %s WHERE cookie_id = %s RETURNING *''',(AsIs(int(group_id)),cookie_id))
    con.commit()
    data = cur.fetchall()
    if data == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"message":"success"}

@app.post('/recommend/',status_code=status.HTTP_201_CREATED, response_model = schemas.Success)
def post_recommendation(recommendation: schemas.Recommendation):
    try:
        cur.execute('''WITH article_data AS (SELECT sk AS id FROM articles WHERE url = %s)
                        INSERT INTO recommendations VALUES (%s, (SELECT id from article_data))'''
                        ,(recommendation.url,AsIs(recommendation.groupid)))
        con.commit()
        return {"message":"success"}
    except Exception as exception:
        print(repr(exception))
        con.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"{repr(exception)}")

@app.post('/summary/',status_code=status.HTTP_201_CREATED, response_model = schemas.Success)
def post_summary(summary: schemas.Summary):
    cur.execute('''UPDATE articles SET summary=%s WHERE url = %s RETURNING *''',(summary.summary,summary.url))
    con.commit()
    result = cur.fetchone()
    if result == None:
        con.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"url {summary.url} not in database")
    return {"message":"success"}

@app.post('/articles/',status_code=status.HTTP_201_CREATED, response_model = schemas.Success)
def post_article(article_data: schemas.Article):
    try:
        cur.execute("""INSERT INTO articles(url,title,text,count,tags,summary,date) VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                [article_data.url,article_data.title,article_data.text,article_data.count,article_data.tags,article_data.summary,article_data.date])
        con.commit()
    except KeyError as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Item {article_data.url} had no key {repr(exception)}")
    except database.pg.IntegrityError as exception:
        con.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail = f'Pipeline raised a {repr(exception)}')
    return {"message":"success"}

@app.post('/rating/', status_code=status.HTTP_201_CREATED, response_model= schemas.Success)
def post_rating(rating: schemas.UserRating):
    try:
        # Get userId associated with cookieId
        cur.execute('''SELECT id FROM users WHERE cookie_id = %s''',(rating.cookieid,))
        id: dict = cur.fetchone()
        if id == None:
            cur.execute('''INSERT INTO users (cookie_id) VALUES (%s) RETURNING id''',(rating.cookieid,))
            id = cur.fetchone()
        id = id['id']

        # Insert value, updates rating if user rated the URL before, returns None if URL doesn't exist in database
        cur.execute('''WITH data AS (SELECT %s AS id,sk,%s AS rating, url FROM articles WHERE url = %s)
                        INSERT INTO users_ratings SELECT id,sk,rating FROM data
                        ON CONFLICT (user_id,article_id) DO UPDATE SET rating = %s
                        RETURNING (SELECT url FROM data), rating ;'''
                        ,(id,rating.rating,rating.url,rating.rating)) 

        con.commit()
    except Exception as e:
        con.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "bad input")

    inserted_data = cur.fetchone()
    if inserted_data == None:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = "Invalid url")
    return {"message":"success"}
