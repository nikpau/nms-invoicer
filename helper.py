from os.path import isfile

def get_eventlist()-> list[str]:
    return ["foo","bar","baz"]

def strip(values: dict) -> list:
    
    event_name = values["event_name"]["static_select-action"]\
        ["selected_option"]["text"]["text"]
        
    event_date = values["event_date"]["datepicker-action"]["selected_date"]
    user = values["user"]["users_select-action"]["selected_user"]
    event_cost = values["event_cost"]["plain_text_input-action"]["value"]
    
    try:
        event_cost = float(event_cost)
    except ValueError:
        raise ValueError("Ungültiges Format. Bitte Englisches Format oder "
                         "Ganzzahl nutzen. Bsp: 2 oder 12.69") 
    
    out = {
        "event_date": event_date,
        "event_name": event_name,
        "event_cost": event_cost,
        "user"      : user
    }
    
    return out


class Datafile:
    def __init__(self, event_name: str) -> None:
        
        datapath = "db/"
        extension = ".data"
        
        self.file = datapath + event_name + extension
        
        if not isfile(self.file):
            self.row_counter = 0
            with open(self.file, "w+"):
                pass

        with open(self.file, "r") as f:
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
            header = ",".join([k for k in d.keys()]) + "\n"
        
        # Build row
        row = ",".join([str(v) for v in d.values()]) + "\n"
        
        
        with open(self.file,"a") as file:
            if self.row_counter == 0:
                file.write(header)
            file.write(row)
        
        self.row_counter += 1