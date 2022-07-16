from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

def summarizer():
    requests.get("http://models:8000/summarizer/")
    return

def recommender():
    requests.get("http://models:8000/recommender/")
    return

def trainer():
    requests.get("http://models:8000/trainer/")
    return

with DAG(dag_id = "airflow_dag",
        start_date = datetime(2022,5,11),
        schedule_interval = "10 22 * * *",
        catchup=False) as dag:
    scrape_and_load = BashOperator(task_id = "scrapy", bash_command="cd /opt/airflow/xmlscraper/ && scrapy crawl xmlscrape")
    summarize = PythonOperator(task_id = "summarizer", python_callable=summarizer)
    recommend = PythonOperator(task_id = "recommender", python_callable=recommender)
    train = PythonOperator(task_id = "trainer", python_callable=trainer)

    scrape_and_load >> summarize >> recommend >> train
