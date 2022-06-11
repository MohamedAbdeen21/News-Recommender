# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

<<<<<<< HEAD
import psycopg2 as pg
=======
>>>>>>> 84798cc (diagram, api endpoints, models)
import requests

class XmlscraperPipeline:
    def process_item(self, item, spider):
        try:
            response = requests.post('http://api:8000/articles/',
                        json = {
                            "url":item["url"],
                            "text": item["text"],
                            "count": item["count"],
                            "title": item["title"],
                            "tags": item["tags"],
                            "date": item["date"],
                            "summary": ""
                            })
            if response.status_code == 400:
                raise KeyError(f'Error {response.status_code} for url {item["url"]}')
            elif response.status_code == 409:
                raise ValueError(f'Duplicate entry found for url: {item["url"]}')
        except (KeyError, ValueError) as exception:
            print(f'{repr(exception)}')
            return item
        except Exception as e:
            print(f'{repr(e)}')
