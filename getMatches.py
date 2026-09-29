import os
from dotenv import load_dotenv
from dbFunctions import getChampId, createMatchesTable, insertMatches
from api_requests import getMatches

load_dotenv()

createMatchesTable()

api_key = os.getenv("API_KEY")
limit = 5
offset = 0
end = 0

rows = getChampId()

champIds = [row[0] for row in rows] 

for champId in champIds:
    matchData = []

    while True:
        data = getMatches(api_key, champIds, offset, limit).json()

        print(f"Start: {data.get("start")}")
        print(f"End: {data.get("end")}")
        print(f"Offset: {offset}")
        print(f"Items#: {len(data.get("items"))}")
        end = data.get("end")
        for item in data.get("items"):
            item_tuple = (item["match_id"], item["region"], item["competition_type"], item["competition_name"], item["teams"]["faction1"]["name"], item["teams"]["faction1"]["faction_id"], item["teams"]["faction2"]["name"], item["teams"]["faction2"]["faction_id"], item.get("started_at"), item["finished_at"], item["best_of"], item["round"], item["faceit_url"])
            matchData.append(item_tuple)

        insertMatches(matchData)

        if (end < (offset+limit)):
            break
        else:
            offset += limit