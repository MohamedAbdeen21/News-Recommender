FROM python:3.10
FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.3.0}

RUN pip install scrapy psycopg2-binary feedparser python-dateutil
RUN scrapy startproject xmlscraper

COPY xmlscrape.py /opt/airflow/xmlscraper/xmlscraper/spiders/xmlscrape.py
COPY rssfeeds.py /opt/airflow/xmlscraper/rssfeeds.py
COPY items.py /opt/airflow/xmlscraper/xmlscraper/items.py
COPY properties.py /opt/airflow/xmlscraper/properties.py
COPY pipelines.py /opt/airflow/xmlscraper/xmlscraper/pipelines.py
COPY settings.py /opt/airflow/xmlscraper/xmlscraper/settings.py

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/xmlscraper/"