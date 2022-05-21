FROM python:3.10

WORKDIR /code

RUN pip install fastapi[all] psycopg2-binary

COPY . /code/api

CMD ["uvicorn", "api.api2:app", "--host", "0.0.0.0"]
