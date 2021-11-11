import pandas as pd

from modbus import get_data
from pathlib import Path
from database import *
from parameters import *

data = pd.DataFrame()
dataRow = pd.DataFrame()
path_csv = Path("./database/myData.csv")
path_sqlite = Path("./database/myData.sqlite")
curr_Size = 0

# delete old databases
if path_csv.is_file():
    del_database(path_csv)
if path_sqlite.is_file():
    del_database(path_sqlite)

# create new database with maxsize
for i in range(10):
    if curr_Size < max_Size:
        dataRow = get_data()
        data = data.append(dataRow)
        curr_Size = store_data_csv(dataRow, path_csv)  # store to .csv
    else:
        print("Database is full: " + str(curr_Size) + " Bytes")
        break

print(data.head())
