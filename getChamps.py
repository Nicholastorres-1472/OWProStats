import os
from dotenv import load_dotenv
from api_requests import getChamps
from dbFunctions import createChampionshipTable, insertChamps

load_dotenv()

# Database set up
createChampionshipTable()

api_key = os.getenv("API_KEY")
owcs_organizer = "f0e8a591-08fd-4619-9d59-d97f0571842e"

try:
    data = getChamps(api_key, owcs_organizer).json()
except:
    print("API call failed.")

champ_data = []


for item in data.get("items"):
    item_tuple = (item["name"], item["championship_id"], item["type"], item["region"], item["current_subscriptions"], item["championship_start"])
    item
    champ_data.append(item_tuple)
    
insertChamps(champ_data)
