from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

def summarizer():
    requests.get("http://models:8000/summarizer/")
    return

with DAG(dag_id = "airflow_dag",
        start_date = datetime(2022,5,11),
        schedule_interval = "10 22 * * *",
        catchup=False) as dag:
    scrape_and_load = BashOperator(task_id = "scrapy", bash_command="cd /opt/airflow/xmlscraper/ && scrapy crawl xmlscrape")
    summarize = PythonOperator(task_id = "summarizer", python_callable=summarizer)

    scrape_and_load >> summarize
