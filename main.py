import datetime as dt

import pandas as pd

from modbus import get_data
from database import store_data

data = pd.DataFrame()
for i in range(10):
    data = data.append(get_data())
    #store_data(data)

print(data.head())
