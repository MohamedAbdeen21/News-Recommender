# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import psycopg2 as pg

class XmlscraperPipeline:

    def open_spider(self,spider):
        self.con = pg.connect("host=pgdatabase dbname=newsscraper port=5432 user=root password=root")
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        try:
            self.cur.execute("""INSERT INTO articles(url,title,text,count,date,tags) VALUES(%s,%s,%s,%s,%s,%s)""",
                        [item['url'],item['title'],item['text'],item['count'],item['date'],item['tags']])
            self.con.commit()
            print('Added article')
        except KeyError as exception:
            print('Item {} had no key {}'.format(item['url'], repr(exception)))
        except pg.IntegrityError as exception:
            self.cur.execute("ROLLBACK")
            print('Pipeline raised a {}'.format(repr(exception)))
        return item

    def close_spider(self,spider):
        self.con.close()
