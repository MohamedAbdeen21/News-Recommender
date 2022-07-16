from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import FastAPI
from diagrams.custom import Custom
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.flowchart import Database
from diagrams.programming.language import JavaScript
from diagrams.onprem.workflow import Airflow

with Diagram(direction="TB"):
    with Cluster("Docker Compose",direction="LR",graph_attr={"labeljust":"R"}):

        with Cluster("Airflow\nlocalhost:8080","LR",graph_attr={"labeljust":"R"}):
            airflow = Airflow()
            scrapy = Custom("(1)\nScrapy","./scrapy.png")
            with Cluster("container","LR", graph_attr={"labeljust":"R"}):
                api2 = FastAPI("models:8000")
                summarizer = Custom("\n(3)\nRecommender","./torch.png")
                recommender = Custom("\n(2)\nSummarizer","./torch.png")

                api2 >> recommender 
                api2 >> summarizer
            
            airflow >> scrapy 
            airflow >> api2

        db = Database("PostgreSQL")
        api = FastAPI("localhost:8000")
        pgadmin = PostgreSQL("PgAdmin\nlocalhost:8081")


        with Cluster("Frontend\nlocalhost:3000",graph_attr={"labeljust":'R'}):
            html = Custom('html', './html.png')
            css = Custom('css', './css.png')
            js = JavaScript('js')
            js >> html
            js >> css

    scrapy >> api
    summarizer >> Edge(node=api,reverse=True,forward=True)
    Edge(node = api, reverse= True, forward= True) >> recommender
    Edge(node = summarizer, reverse= True, forward= True) >> api
    Edge(node = js, reverse=True, forward=True) >> api
    Edge(node = api, reverse=True, forward=True) >> db
    Edge(node = db, reverse=True, forward=True) >> pgadmin
