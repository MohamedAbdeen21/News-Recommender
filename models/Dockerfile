FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-devel
WORKDIR /work
RUN pip install fastapi[all] pandas requests transformers

COPY summarizer_script.py /work/summarizer_script.py
COPY api.py /work/api.py

CMD ["uvicorn","api:app","--host","0.0.0.0"]