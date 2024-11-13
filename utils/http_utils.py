import requests
import json



def make_get_request(url) -> dict:
    response = requests.get(url)
    if response.status_code != 200:
        return []
    dict = json.loads(response.text)
    return dict