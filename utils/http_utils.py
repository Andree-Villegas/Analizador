import requests
import json



def make_get_request(url) -> dict:
    x = requests.get(url)
    dict = json.loads(x.text)
    return dict