from pymongo import MongoClient


DEBUG = True
client = MongoClient('mongodb://%s:%s@127.0.0.1' % ('premchand', 'root'))
DATABASE =client['Bank'] # DB_NAME
