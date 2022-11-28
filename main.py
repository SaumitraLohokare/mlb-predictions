from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv

import os

load_dotenv()

client = MongoClient("mongodb+srv://" + os.getenv("U_NAME") + ":" + os.getenv("PASS") + "@mlb-predictions.caflwws.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client["test"]
coll = db["test"]
val = coll.find_one({'name': 'Yankees'})


print(val)
