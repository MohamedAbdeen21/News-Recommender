from fastapi import FastAPI, status
import summarizer_script as summarizer
# import recommedation_script as recommender

app = FastAPI()

@app.get('/summarizer/', status_code=status.HTTP_200_OK)
async def summarize():
    summarizer.run()
    return

<<<<<<< HEAD
=======
# Provide a custom date, in case an error occurred and a day was skipped 
@app.get('/summarizer_custom/{date}', status_code=status.HTTP_200_OK)
async def summarize(date: str):
    summarizer.run(date)
    return

>>>>>>> 84798cc (diagram, api endpoints, models)
@app.get('/recommender/', status_code=status.HTTP_200_OK)
def recommend():
    # recommender.run()
    return
