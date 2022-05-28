from decouple import config
from flask import Flask
import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

client = pymongo.MongoClient(config('MONGO_URI'))
db = client["Test"]



from app import routers