from decouple import config
from flask import Flask
import pymongo
from cas import CASClient

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

client = pymongo.MongoClient(config('MONGO_URI'))
db = client["Test"]

cas_client = CASClient(
    version=3,
    service_url='http://localhost:5000/cas/login?next=%2Fabout',
    server_url=''
)

from app import routers