import json
from datetime import datetime
from typing import Dict
from copy import deepcopy
from json_blocks import __path__

# Create a json string with all current nms events in it
# in order to be available drop-down options in the modal
def create_event_list(eventdata: dict) -> list[dict]:
    
    # Basic Slack conform dropdown layout
    base = {
        "text": {
            "type": "plain_text",
            "text": "",
            "emoji": True
        },
        "value": ""
    }
    
    out = []
    names = eventdata["names"]
    slugs = eventdata["slugs"]
    
    # Create a json object of shape 'base' for 
    # every event in our list
    for idx, event in enumerate(names):
        tmp = deepcopy(base)
        tmp["text"]["text"] = str(event)
        tmp["value"] = slugs[idx]
        out.append(tmp)
    
    return out

def prepare_modal(json_event_list: str) -> Dict:
    
    file = __path__[0] + "/invoice_modal_greeter.json"
    
    with open(file,"r") as modal:
        obj = json.load(modal)
        
    obj["blocks"][2]["accessory"]["options"] = json_event_list
    obj["blocks"][3]["accessory"]["initial_date"] = datetime.today().strftime('%Y-%m-%d')
    
    with open(file, "w") as outfile:
        json.dump(obj,outfile)
        
    return json.dumps(obj)
    
    