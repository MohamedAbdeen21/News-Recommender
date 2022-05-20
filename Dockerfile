FROM python:3.10
FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.3.0}

RUN pip install scrapy psycopg2-binary feedparser python-dateutil
RUN scrapy startproject xmlscraper

COPY scraper/xmlscrape.py /opt/airflow/xmlscraper/xmlscraper/spiders/xmlscrape.py
COPY scraper/rssfeeds.py /opt/airflow/xmlscraper/rssfeeds.py
COPY scraper/items.py /opt/airflow/xmlscraper/xmlscraper/items.py
COPY scraper/properties.py /opt/airflow/xmlscraper/properties.py
COPY scraper/pipelines.py /opt/airflow/xmlscraper/xmlscraper/pipelines.py
COPY scraper/settings.py /opt/airflow/xmlscraper/xmlscraper/settings.py

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/xmlscraper/"