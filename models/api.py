from fastapi import FastAPI, status
import summarizer_script as summarizer
# import recommedation_script as recommender

app = FastAPI()

@app.get('/summarizer/', status_code=status.HTTP_200_OK)
async def summarize():
    summarizer.run()
    return

@app.get('/recommender/', status_code=status.HTTP_200_OK)
def recommend():
    # recommender.run()
    return
