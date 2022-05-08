from typing import List
from models import EventSlug, Invoice
import os
from os.path import isdir

datapath = "db/"
extension = ".json"

def get_path(slug: EventSlug) -> str:
    return datapath + slug + extension

def write_invoices(slug: EventSlug, invoices: List[Invoice]) -> None:
    if not isdir(datapath):
        os.mkdir(datapath)
    
    path = get_path(slug)
    with open(path, "w+") as f:
      json = Invoice.schema().dumps(invoices, many=True)
      f.write(json)

def read_invoices(slug: EventSlug) -> List[Invoice]:
  path = get_path(slug)
  with open(path, "r") as f:
    return Invoice.schema().loads(f.read(), many=True)