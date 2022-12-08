from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from itertools import combinations

from data_importer import import_from_csv
from calculations import calculate

from dotenv import load_dotenv
import pp

import os

load_dotenv()

# Connecting to MongoDB
client = MongoClient("mongodb+srv://" + os.getenv("U_NAME") + ":" + os.getenv("PASS") + "@mlb-predictions.caflwws.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client["mlb"]
pitching_coll = db["pitching"]
batting_coll = db["batting"]

# Importing data sets
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

# Task 1
oRPB = calculate(batting_coll)
# Task 2
dRPB = calculate(pitching_coll)

# Filter teams that are in playoffs
oRPB_playoffs = { k:v for k, v in oRPB.items() if k in playoff_teams }
dRPB_playoffs = { k:v for k, v in dRPB.items() if k in playoff_teams }

# playoff matches combinations
matches = list(combinations(playoff_teams, 2))

# Simulate matches --> Task 3
def predict_winner(teams) -> str:
    first_half = oRPB_playoffs[teams[0]] - dRPB_playoffs[teams[1]]
    second_half = oRPB_playoffs[teams[1]] - dRPB_playoffs[teams[0]]
    if first_half > second_half:
        return teams[0]
    else:
        return teams[1]

wildcard_brackets = [
    ("Tampa Bay Rays", "Cleveland Guardians"),
    ("Seattle Mariners", "Toronto Blue Jays"),
    ("Philadelphia Phillies", "St. Louis Cardinals"),
    ("San Diego Padres", "New York Mets")
]

divisional_brackets = [
    ("New York Yankees", predict_winner(wildcard_brackets[0])),
    ("Houston Astros", predict_winner(wildcard_brackets[1])),
    ("Atlanta Braves", predict_winner(wildcard_brackets[2])),
    ("Los Angeles Dodgers", predict_winner(wildcard_brackets[3])),
]

championship_brackets = [
    (predict_winner(divisional_brackets[0]), predict_winner(divisional_brackets[1])),
    (predict_winner(divisional_brackets[2]), predict_winner(divisional_brackets[3])),
]

overall_winner = predict_winner((predict_winner(championship_brackets[0]), predict_winner(championship_brackets[1])))

pp(wildcard_brackets)
print()
pp(divisional_brackets)
print()
pp(championship_brackets)
print()
print(overall_winner)