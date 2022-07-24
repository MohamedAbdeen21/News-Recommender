FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-devel
WORKDIR /work
# Summarirzer and API
RUN pip install fastapi[all] requests transformers pandas
# Recommender
RUN pip install scipy scikit-learn gensim nltk

ADD recommender/ /work/
COPY summarizer_script.py /work/summarizer_script.py
COPY api.py /work/api.py

CMD ["uvicorn","api:app","--host","0.0.0.0"]