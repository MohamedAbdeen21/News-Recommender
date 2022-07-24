from fastapi import FastAPI, status
import summarizer_script as summarizer
import LDA_Generation as recommender
import LDA_Training as trainer

app = FastAPI()

@app.get('/summarizer/', status_code=status.HTTP_200_OK)
def summarize():
    summarizer.run()
    return

# Provide a custom date, in case an error occurred and a day was skipped 
@app.get('/summarizer_custom/{date}/', status_code=status.HTTP_200_OK)
def summarize(date: str):
    summarizer.run(date)
    return

@app.get('/recommender/', status_code=status.HTTP_200_OK)
def recommend():
    recommender.run()
    return

@app.get('/recommender_custom/{date}/', status_code=status.HTTP_200_OK)
def recommend(date: str):
    recommender.run(date)
    return

@app.get('/trainer/',status_code=status.HTTP_200_OK)
def train():
    trainer.run()
    return
