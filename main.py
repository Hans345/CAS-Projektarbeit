import datetime as dt

import pandas as pd

from modbus import get_data

data = pd.DataFrame()
for i in range(10):
    data = data.append(get_data())

print(data.head())
