import pymongo
import pandas as pd 
import json
import os
from dataclasses import dataclass


@dataclass
class EnvirontVariable:
    mongo_db_url:str=os.getenv("MONGO_DB_URL")

env_var = EnvirontVariable()
#print(env_var.mongo_db_url)
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)

