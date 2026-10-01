import requests

def getChamps(api_key, organizer_id):
    url = f"https://open.faceit.com/data/v4/organizers/{organizer_id}/championships"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    query_params = {
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=query_params)
    
    return response