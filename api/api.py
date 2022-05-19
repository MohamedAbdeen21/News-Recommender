from flask import Flask, request
from flask_restful import Resource, Api
import psycopg2 as pg
from psycopg2.extensions import AsIs

class Result:
    def __new__(self,query, offset):
        self.keys = ['sk','url','title','text','count','tags']

        self.con = pg.connect("host=pgdatabase dbname=newsscraper port=5432 user=root password=root")
        self.cur = self.con.cursor()
        self.result = self.cur.execute("SELECT %s FROM articles WHERE date=%s OFFSET %s LIMIT 5",(AsIs(",".join(self.keys)),query,offset))
        self.result = self.cur.fetchall()
        self.k = 0
        self.dict_result = {}
        for values in self.result:
            self.k += 1
            self.dict_result[f"item {self.k}"]= dict(zip(self.keys,values))
        return self.dict_result

app = Flask(__name__)
api = Api(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

class Article(Resource):
    def get(self,date,offset):
        return Result(date,offset), 200

api.add_resource(Article, "/Article/<string:date>/<int:offset>")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')