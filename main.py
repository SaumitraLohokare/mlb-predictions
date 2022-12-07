from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from itertools import combinations

from data_importer import import_from_csv
from calculations import calculate

from dotenv import load_dotenv
import pp

import os

load_dotenv()

client = MongoClient("mongodb+srv://" + os.getenv("U_NAME") + ":" + os.getenv("PASS") + "@mlb-predictions.caflwws.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client["mlb"]
pitching_coll = db["pitching"]
batting_coll = db["batting"]

data_pitching = import_from_csv('team_standard_pitching.csv')
data_batting = import_from_csv('team_standard_batting.csv')

playoff_teams = (
    "Atlanta Braves",
    "Cleveland Guardians",
    "Houston Astros",
    "Los Angeles Dodgers",
    "New York Mets",
    "New York Yankees",
    "Philadelphia Phillies",
    "San Diego Padres",
    "Seattle Mariners",
    "St. Louis Cardinals",
    "Tampa Bay Rays",
    "Toronto Blue Jays"
)

oRPB = calculate(batting_coll)
dRPB = calculate(pitching_coll)

# Filter teams that are in playoffs
oRPB_playoffs = { k:v for k, v in oRPB.items() if k in playoff_teams }
dRPB_playoffs = { k:v for k, v in dRPB.items() if k in playoff_teams }

# playoff matches combinations
matches = list(combinations(playoff_teams, 2))

# Simulate matches
for match in matches:
    print("----------", match[0], " vs", match[1], "----------")
    first_half = oRPB_playoffs[match[0]] - dRPB_playoffs[match[1]]
    second_half = oRPB_playoffs[match[1]] - dRPB_playoffs[match[0]]

    print(first_half, second_half)
    if first_half > second_half:
        print("Winner: ", match[0])
    else:
        print("Winner: ", match[1])
    print()