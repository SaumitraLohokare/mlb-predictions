from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from data_importer import import_from_csv

from dotenv import load_dotenv

import os

load_dotenv()

client = MongoClient("mongodb+srv://" + os.getenv("U_NAME") + ":" + os.getenv("PASS") + "@mlb-predictions.caflwws.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client["mlb"]
coll = db["pitching"]

data_pitching = import_from_csv('team_standard_pitching.csv')
data_batting = import_from_csv('team_standart_batting.csv')