from os.path import isfile

def get_eventlist()-> list[str]:
    return ["foo","bar","baz"]

def strip(values: dict) -> list:
    
    event_name = values["event_name"]["static_select-action"]\
        ["selected_option"]["text"]["text"]
        
    invoice_date = values["event_date"]["datepicker-action"]["selected_date"]
    user = values["user"]["users_select-action"]["selected_user"]
    cost = values["invoice_cost"]["plain_text_input-action"]["value"]
    purpose = values["purpose"]["purpose"]["value"]
    
    # Capitalize first letter
    purpose = purpose[0].upper() + purpose[1:]
    
    try:
        cost = float(cost)
    except:
        raise ValueError("Wo Sinn? Bitte Ganzzahl oder "
                         "Englisches Format nutzen. Bsp: 2 oder 12.69") 
    
    if str(cost)[::-1].find(".") > 2:
        raise ValueError("Mehr als zwei Nachkommastellen gibt es "
                         "nicht amk.")
    
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
            self.row_counter = 0
            with open(self.filename, "w+"):
                pass

        with open(self.filename, "r") as f:
            self.row_counter = sum(1 for line in f)

    def store(self, d: dict) -> None:
        """Store a given invoice dict to the event data file.
        If it does not exist yet, build it.

        Args:
            d (dict): Invoice dict containg:
                        - Event Name
                        - Event Date
                        - Event Cost
                        - User
            
        """

        # Build a header if the file is new
        if self.row_counter == 0:
            header = ",".join([k for k in d.keys()])
        
        # Build row
        row = ",".join([str(v) for v in d.values()])
        
        
        with open(self.filename,"a") as file:
            if self.row_counter == 0:
                file.write(header + "\n")
            file.write(row + "\n")
        
        self.row_counter += 1