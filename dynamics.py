import json
from typing import Dict
from copy import deepcopy
from json_blocks import __path__

# Create a json string with all current nms events in it
# in order to be available drop-down options in the modal
def create_event_list(events: list) -> list:
    
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
    
    # Create a json object of shape 'base' for 
    # every event in our list
    for idx, event in enumerate(events):
        tmp = deepcopy(base)
        tmp["text"]["text"] = str(event)
        tmp["value"] = "value-" + str(idx)
        out.append(tmp)
    
    return out

def push_event_list(json_event_list: str) -> Dict:
    
    file = __path__[0] + "/invoice_modal_greeter.json"
    
    with open(file,"r") as modal:
        obj = json.load(modal)
        
    obj["blocks"][2]["accessory"]["options"] = json_event_list
    
    with open(file, "w") as outfile:
        json.dump(obj,outfile)
        
    return json.dumps(obj)
    
    