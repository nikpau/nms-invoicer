import json
import requests


def get_events():
    # Get the events from the API
    data = requests.get("https://api.nms-ev.org/items/events").content
    data = json.loads(data)['data']
    converted = {
        v['slug']: v
        for v in data
    }
    return converted