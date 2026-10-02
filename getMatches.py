import os, time
from dotenv import load_dotenv
from dbFunctions import getChampId, createMatchesTable, insertMatches, exist
from api_requests import getMatches

load_dotenv()

createMatchesTable()

api_key = os.getenv("API_KEY")

rows = getChampId()

champIds = [row[0] for row in rows] 

champnum = 0

for champId in champIds:
    matchData = []
    limit = 100
    offset = 0
    end = 0
    totalFailedInserts = 0
    
    print(f"Champ: {champId}")
    
    if exist("matches", "champ_id", champId):
        continue
    
    while True:
        time.sleep(0.1)
        failedInserts = 0
        data = getMatches(api_key, champId, offset, limit).json()
        items = data.get("items")
        if items is None:
            break

        # print(f"Start: {data.get("start")}")
        # print(f"End: {data.get("end")}")
        # print(f"Offset: {offset}")
        
        itemCount = len(data.get("items"))
        for item in data.get("items"):
            item_tuple = (item["match_id"], item["region"], item["competition_type"], item["competition_name"], item["teams"]["faction1"]["name"], item["teams"]["faction1"]["faction_id"], item["teams"]["faction2"]["name"], item["teams"]["faction2"]["faction_id"], item.get("started_at"), item.get("finished_at"), item["best_of"], item["round"], champId)
            matchData.append(item_tuple)

        failedInserts = insertMatches(matchData)
        if (failedInserts > 0):
            print(f"Items#: {len(items)}")
            print(failedInserts)
        
        totalFailedInserts += failedInserts

        if (itemCount < (limit)):
            break
        else:
            offset += limit