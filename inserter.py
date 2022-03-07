import subprocess
import os
from time import sleep
from datetime import datetime
from os.path import isdir

class InvalidFormatError(Exception):
    pass

class NotSetError(Exception):
    pass

class LatexBuilder:
    def __init__(self, datafile: str) -> None:
        """Initialize a Latex Builder Object 
        from a given data file path. 
        
        The data is written into a dict of the
        following form:
            out = {
                "invoice_date": [],
                "event_name"  : [],
                "purpose"     : [],
                "cost"        : [],
                "user"        : []
            }

        Args:
            datafile (str): File path of the data file 
            for a single event
        """
        
        if not datafile.endswith(".data"):
            raise InvalidFormatError("Wrong file fromat. "
                                     "Can only generate LatexBuilder from '.data' files.")
        
        self.data_size = 0
        
        # Indicate wether the 'set()' method has
        # already been called and the data is ready
        # for compilation
        self.is_set = False
    
        with open(datafile, "r") as f:
            for idx, line in enumerate(f):
                line = line.rstrip() # rm \n
                if idx == 0:
                    header = line.split(",")
                    self.data = {key:[] for key in header}
                else:
                    entry = line.split(",")
                    for pair in zip(header,entry):
                        key, val = pair
                        self.data[key].append(val)
                    self.data_size += 1
        
        # Total spent on the event as sum of costs (Duh)
        # TODO Use integers to represent the amount rathe that floats
        self.total = str(round(sum(float(price) for price in self.data["cost"]),2))
        
        # Transform date list to actual dates
        self.dates = [datetime.strptime(d,"%Y-%m-%d") for d in self.data["invoice_date"]]
        
        # Extract Event Name as fist entry of event_name list.
        # Strip all whitespaces and make all lowercase
        self.event_name = str(self.data["event_name"][0])
        self.event_name = self.event_name.lower().replace(" ","")
        
    def sort_by_date(self) -> None:
        
        # Get argsorted indices for dates
        indices = self.argsort(self.dates)
        
        # Argsort by dates
        for key, val in self.data.items():
            self.data[key] = [val[s] for s in indices]
            
        # Make the dates strings again to parse them later
        self.dates = [datetime.strftime(d,"%d.%m.%Y") for d in self.dates]
            
    def pad_prices(self) -> None:
        """Pad zeros to the end of every price 
        for alignment of euro and cents

        """

        # Append total to inlude in padding
        self.data["cost"].append(self.total)
        
        for idx, price in enumerate(self.data["cost"]):
            if price.endswith(".0"):
                self.data["cost"][idx] += "0"
                
        self.total = self.data["cost"][-1]
        self.data["cost"].pop()
                
    def set(self) -> None:
        """Write all event data into the respective 
        .tex files without compiling

        """
        
        prefix = "tex/blocks/"
        
        self.sort_by_date()
        self.pad_prices()
        
        # Open file to write all submitted invoices one per line
        cost_list = open(prefix + "tableitems.tex", "w")
        invoice = zip(self.data["purpose"], 
                      self.data["invoice_date"], 
                      self.data["cost"])
        
        for _ in range(self.data_size):
            line = self.build_list_entry(*next(invoice))
            cost_list.write(line + "\n")
        cost_list.close()
        
        # Write event name
        with open(prefix + "eventname.tex", "w") as ev:
            ev.write(self.event_name[0].upper() + self.event_name[1:])
            
        with open(prefix + "eventdate.tex", "w") as dt:
            dt.write("NOT IMPLEMENTED")
        
        with open(prefix + "total.tex", "w") as tot:
            tot.write(self.total)
            
        self.is_set = True
            
    def compile(self, debug: bool = False) -> None:
        
        if not self.is_set:
            raise NotSetError("No data to compile. "
                              "Set the data by calling 'set()' first")

        tex_dir = "./tex/"
        output_dir = "./out/"
        
        if not isdir(output_dir):
            os.mkdir(output_dir)
        
        # Write to pdf using pdflatex
        subprocess.check_call(
            [
                "pdflatex", 
                "-interaction=batchmode",
                f"-output-directory={output_dir}",
                f"-jobname={self.event_name}",
                f"{tex_dir}main.tex"
            ]
        )
        
        if not debug:
            self.cleanup()
            
    def cleanup(self) -> None:
        
        wd = os.getcwd()
        
        out = wd + "/out/"
        tex = wd + "/tex/"
        
        for dir in [out,tex]:
            for extension in [".aux", ".log",".out"]:
                subprocess.check_call([
                    "rm",
                    "-f",
                    f"{dir}*{extension}"
                ])
            
            
    # Construct a list entry formatted as tabularx
    @staticmethod
    def build_list_entry(purpose: str, date: str, price: str) -> str:
        l = purpose + "&" + date + "&\\amount{" + str(price) + "}\\" + "\\"
        return l

    # Importing numpy just for an argsort seems to much
    # Therefore a quick impl in base python
    @staticmethod
    def argsort(seq: list):
        return sorted(range(len(seq)), key=seq.__getitem__)