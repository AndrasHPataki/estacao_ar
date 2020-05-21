from flask import Flask, request,redirect,jsonify,render_template
import mongoengine as me
from mongoengine import connect,Document,StringField,IntField,DateTimeField
from pymongo import MongoClient
from flask_restful import Resource, Api
from flask_restful import reqparse
from datetime import date, datetime
from datetime import datetime

import datetime
database = "test"
db_uri = "mongodb+srv://andras:563D@cluster0-ztzvh.mongodb.net/test?retryWrites=true&w=majority"
db = connect(database, host=db_uri)

class AirApi(Document):
    #id = StringField(required=True, primary_key=True)
    umidade = IntField()
    temperatura = IntField()
    date = DateTimeField(default=datetime.datetime.now)
  


app = Flask(__name__)
api = Api(app)

my_data = AirApi()

def query_all():
    result = []
    for x in AirApi.objects:
        result.append({'umidade': x.umidade, 'temperatura': x.temperatura, 'data': x.date})
    return result

@app.route('/api/v1/views/')
def home():
    result = query_all()
    return render_template('index.html', result=result)


class Collector(Resource):
    def get(self):
        result = query_all()
        return jsonify(result)
        
        
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("temperatura",type=int, location='json', required=True, help="Informe a Temperatura")
        parser.add_argument("umidade",type=int, location='json', required=True, help="Informe a Umidade!")
       
        args = parser.parse_args()
        
        my_data.temperatura = args['temperatura']
        my_data.umidade = args['umidade']
       
        my_data.date = datetime.datetime.now()
        my_data.save(force_insert=True)
        return args
        


#my_data.text = "Hello World!"
#my_data.name_a = "Andras"
#my_data.year = 2020
#my_data.save()
    
api.add_resource(Collector, '/api/v1/')


if __name__ == '__main__':
    app.run(debug=True)
