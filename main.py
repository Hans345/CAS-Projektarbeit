import pandas as pd

from modbus import get_data
from pathlib import Path
from database import *
from parameters import *

data = pd.DataFrame()
dataRow = pd.DataFrame()
my_dir = Path("./database/")
my_file = Path("./database/myData.csv")
curr_Size = 0

# delete old database
if my_file.is_file():
    del_database()

# create new database with maxsize
for i in range(10):
    data = data.append(get_data())
    dataRow = get_data()
    if curr_Size < max_Size:
        curr_Size = store_data(dataRow)
    else:
        print("Database is full: " + str(curr_Size) + "Bytes")
        break

print(data.head())
