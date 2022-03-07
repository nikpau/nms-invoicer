from os.path import isfile
from datetime import datetime

class InputError(Exception):
    pass

def get_eventlist()-> list[str]:
    return ["foo","bar","baz"]

def strip(values: dict, user_id: str) -> list:
    
    event_name = values["event_name"]["static_select-action"]\
        ["selected_option"]["text"]["text"]
        
    invoice_date = values["event_date"]["invoice-date-select"]["selected_date"]
    user = user_id
    cost = values["invoice_cost"]["plain_text_input-action"]["value"]
    purpose = values["purpose"]["purpose"]["value"]
    
    # Capitalize first letter
    purpose = purpose[0].upper() + purpose[1:]
    
    
    try:
        cost = float(cost)
    except:
        raise InputError("Bitte Ganzzahl oder "
                         "Englisches Format nutzen. Bsp: 2 oder 12.69",
                         "invoice_cost") 
    
    if str(cost)[::-1].find(".") > 2:
        raise InputError("Mehr als zwei Nachkommastellen gibt es "
                         "nicht amk.", "invoice_cost")
    
    out = {
        "invoice_date": invoice_date,
        "event_name"  : event_name,
        "purpose"     : purpose,
        "cost"        : cost,
        "user"        : user
    }
    
    return out


class Datafile:
    def __init__(self, event_name: str) -> None:
        
        datapath = "db/"
        extension = ".data"
        
        self.filename = datapath + event_name + extension
        
        if not isfile(self.filename):
            self.is_new_file = True
            with open(self.filename, "w+"):
                pass

    def store(self, d: dict) -> None:
        """Store a given invoice dict to the event data file.
        If it does not exist yet, build it.

        Args:
            d (dict): Invoice dict containg:
                        - Event Name
                        - Event Date
                        - Invoice Cost
                        - User
            
        """

        # Build a header if the file is new
        if self.is_new_file:
            header = ",".join([k for k in d.keys()])
        
        # Build row
        row = ",".join([str(v) for v in d.values()])
        
        
        with open(self.filename,"a") as file:
            if self.is_new_file:
                file.write(header + "\n")
            file.write(row + "\n")
        
        self.is_new_file = False