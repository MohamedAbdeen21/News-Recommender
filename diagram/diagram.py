from diagrams import Diagram, Cluster
from diagrams.programming.framework import FastAPI, Flask
from diagrams.custom import Custom
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.flowchart import Database

with Diagram(direction="TB"):
    with Cluster("Docker",direction="TB",graph_attr={"labeljust":"R"}):
        with Cluster("Airflow\nlocalhost:8080","LR",graph_attr={"labeljust":"R"}):
            recommender = Custom("(3)\nRecommender","./tensorflow.png")
            summarizer = Custom("(2)\nSummarizer","./tensorflow.png")
            scrapy = Custom("(1)\nScrapy","./scrapy.png")


        db = Database("PostgreSQL")
        api = FastAPI("localhost:8000")
        pgadmin = PostgreSQL("PgAdmin\nlocalhost:8081")


        with Cluster("Frontend",graph_attr={"labeljust":'R'}):
            html = Custom('html', './html.png')
            css = Custom('css', './css.png')
            flask = Flask()

    scrapy >> api
    summarizer >> api >> summarizer
    api >> recommender >> api
    flask >> api >> flask
    api >> db >> api
    pgadmin >> db >> pgadmin
