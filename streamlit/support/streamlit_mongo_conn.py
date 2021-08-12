from pymongo import MongoClient
import os
import sys
sys.path.append(os.path.abspath(".."))
from src.config import mongo_url

client = MongoClient(mongo_url)
database = client.get_database("bdmlpt0521midproject")
