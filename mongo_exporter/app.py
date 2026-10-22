import os
import time
from prometheus_client import start_http_server, Gauge
from pymongo import MongoClient

MONGODB_URI = os.environ['MONGODB_URI']

UP = Gauge('mongodb_up', 'MongoDB up (1 = up, 0 = down)')
COLLECTIONS = Gauge('mongodb_collections_count', 'Number of collections in monitored DB')

def check():
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
        db = client.get_default_database()
        cols = db.list_collection_names()
        UP.set(1)
        COLLECTIONS.set(len(cols))
    except Exception:
        UP.set(0)

if __name__ == '__main__':
    start_http_server(9216)
    while True:
        check()
        time.sleep(15)
