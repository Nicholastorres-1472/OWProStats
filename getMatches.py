import os
from dotenv import load_dotenv
from dbFunctions import getChampId, createMatchesTable, insertMatches
from api_requests import getMatches

load_dotenv()

createMatchesTable()

api_key = os.getenv("API_KEY")

rows = getChampId()

champIds = [row[0] for row in rows] 

for champId in champIds:
    matchData = []
    limit = 1
    offset = 0
    end = 0
    
    while True:
        data = getMatches(api_key, champId, offset, limit).json()

        print(f"Start: {data.get("start")}")
        print(f"End: {data.get("end")}")
        print(f"Offset: {offset}")
        print(f"Items#: {len(data.get("items"))}")
        itemCount = len(data.get("items"))
        for item in data.get("items"):
            item_tuple = (item["match_id"], item["region"], item["competition_type"], item["competition_name"], item["teams"]["faction1"]["name"], item["teams"]["faction1"]["faction_id"], item["teams"]["faction2"]["name"], item["teams"]["faction2"]["faction_id"], item.get("started_at"), item.get("finished_at"), item["best_of"], item["round"], item["faceit_url"], champId)
            matchData.append(item_tuple)

        insertMatches(matchData)

        if (itemCount < (limit)):
            break
        else:
            offset += limit