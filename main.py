import datetime as dt

import pandas as pd

from modbus import get_data
from database import store_data, del_database

max_Size = 400  # 100 * 10 ** 6  # 100 MB
curr_Size = 0

data = pd.DataFrame()
del_database()
for i in range(10):
    data = data.append(get_data())
    if curr_Size < max_Size:
        curr_Size = store_data(data)
    else:
        print("Database is full: " + str(curr_Size) + "Bytes")
        break

print(data.head())
