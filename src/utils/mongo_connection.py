from pymongo import MongoClient
import os
import sys
sys.path.append(os.path.abspath("."))
from config import mongo_url
from utils.json_response import str_to_json

client = MongoClient(mongo_url)

def mongo_read(db, coll, query={}, project=None, client=client):
    for k, v in query.items():
        if "{" in v:
            query[k] = str_to_json(v)
    print(query)
    collection = client.get_database(db)[coll]
    return collection.find(query,project)


