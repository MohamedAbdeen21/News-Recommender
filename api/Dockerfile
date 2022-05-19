FROM python:3.10

RUN pip install flask_restful flask flask-sqlalchemy psycopg2-binary

COPY api.py /api.py

CMD ["python3", "/api.py"]