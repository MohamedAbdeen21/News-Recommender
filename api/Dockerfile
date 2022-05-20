FROM python:3.10

WORKDIR /code

RUN pip install fastapi[all] psycopg2-binary

COPY . /code/app

CMD ["uvicorn", "app.api2:app", "--host", "0.0.0.0"]
