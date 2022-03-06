import json
import sys
from datetime import datetime

json_path = sys.argv[1]

# only for testing
# json_path = "MOCK_DATA.json"

with open(json_path) as j:
    raw_data = json.load(j)
    
data_size = len(raw_data)

# Dict for the json entries
data = {
    "item": [],
    "date": [],
    "price": []
}
    
# Fill the lists with their respective entries
for key,_ in data.items():
    for entry in range(data_size):
        data[key].append(raw_data[entry][key])

TOTAL_SPENT = sum(data["price"])


# Transform date list to actual date in order to 
# perform an argsort on them
data["date"] = [datetime.strptime(x,"%Y-%m-%d") for x in data["date"]]

# Importing numpy just for an argsort seems to much
# Therefore a quick impl in base python
def argsort(seq: list):
    return sorted(range(len(seq)), key=seq.__getitem__)

# Argsort by date to get an index list for the other list
# to be sorted by
sorted_idx = argsort(data["date"])

# Argsort by dates
for key, val in data.items():
    data[key] = [val[s] for s in sorted_idx]
   
# Convert dates back to string 
data["date"] = [datetime.strftime(d,"%d.%m.%Y") for d in data["date"]]
    
# Pad zeros to the end of every price 
# for alignment of euro and cents
data["price"] = [str(price) + ".00" if "." not in str(price) else str(price) for price in data["price"]]

# Construct a list entry formatted as tabularx
def build_list_entry(item: str, date: str, price: str) -> str:
    l = item + "&" + date + "&\\amount{" + str(price) + "}\\" + "\\"
    return l

# Write the item lines to file
tex_list = open("tex/blocks/table_items.tex","w")
arg_iterator = zip(data["item"],data["date"],data["price"])
for _ in range(data_size):
    line = build_list_entry(*next(arg_iterator))
    tex_list.write(line +"\n")
tex_list.close()

# Write total amount to file
with open("tex/blocks/total.tex", "w") as tot:
    tot.write("\\amount{" + str(TOTAL_SPENT) + "}")
