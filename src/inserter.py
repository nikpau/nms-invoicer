from models import Event
import subprocess
import os
from os.path import isdir
from typing import List

from helper import Invoice

class InvalidFormatError(Exception):
    pass


class NotSetError(Exception):
    pass


class LatexBuilder:
    event: Event
    invoices: List[Invoice]
    is_set: bool = False

    def __init__(self, event: Event, invoices: List[Invoice]) -> None:
        self.event = event
        self.invoices = invoices 

    def event_name(self) -> str:
      return self.event.slug.replace('-', ' ').capitalize()

    def total(self) -> str:
        """
        Total spent on the event as sum of costs (Duh)
        # TODO Use integers to represent the amount rathe that floats
        """
        return str(round(sum(float(invoice.cost)
                         for invoice in self.invoices), 2))

    def set(self):
        """Write all event data into the respective 
        .tex files without compiling
        """
        prefix = "tex/blocks/"
        
        # Open file to write all submitted invoices one per line
        with open(prefix + "tableitems.tex", "w") as cost_list:
          for invoice in self.invoices:
              line = self.build_list_entry(invoice)
              cost_list.write(line + "\n")

        # Write event name
        with open(prefix + "eventname.tex", "w") as ev:
            ev.write(self.event_name())

        with open(prefix + "eventdate.tex", "w") as dt:
            dt.write(self.event.date.strftime("%d.%m.%Y"))

        with open(prefix + "total.tex", "w") as tot:
            tot.write("\\amount{" + self.total() + "}")

        self.is_set = True
        return self

    def compile(self, debug: bool = False) -> None:
        if not self.is_set:
            raise NotSetError("No data to compile. "
                              "Set the data by calling 'set()' first")

        tex_dir = "./tex/"
        output_dir = "./out/"

        if not isdir(output_dir):
            os.mkdir(output_dir)

        jobname = self.event_name().replace("_", "-")

        if subprocess.call(['which', 'tectonic']) == 0:
            out = f"{output_dir}{jobname}"
            os.makedirs(out, exist_ok=True)
            subprocess.check_call(
                [
                    "tectonic",
                    f"{tex_dir}main.tex",
                    "-o", out,
                ]
            )
        elif subprocess.call(['which', 'pdflatex']) == 0:
            subprocess.check_call(
                [
                    "pdflatex",
                    "-interaction=batchmode",
                    f"-output-directory={output_dir}",
                    f"-jobname={jobname}",
                    f"{tex_dir}main.tex"
                ]
            )

        if not debug:
            extensions = ["aux", "log", "out", "gz"]
            for extension in extensions:
                subprocess.check_call(
                    ["find",
                     ".",
                     "-name", f"*.{extension}",
                     "-type",
                     "f",
                     "-delete"])

    # Construct a list entry formatted as tabularx
    @staticmethod
    def build_list_entry(invoice: Invoice) -> str:
        return f"{invoice.purpose}&{invoice.date.strftime('%Y.%m.%d')}&\\amount{{{invoice.cost:.2f}}}\\\\"

    # Importing numpy just for an argsort seems to much
    # Therefore a quick impl in base python
    @staticmethod
    def argsort(seq: list):
        return sorted(range(len(seq)), key=seq.__getitem__)
