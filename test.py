import datetime as dt
import pandas as pd
import numpy as np

data = np.array(np.zeros(3), dtype=float)[np.newaxis]
data[0,0] = 1
data[0,1] = 2
data[0,2] = 3
s = (["data1", "data2", "data3"])
df = pd.DataFrame(data, columns=s)
df = df.assign(time=dt.datetime.now())
df['time'] = pd.to_datetime(df['time'])
typ = df.dtypes
df = df.set_index('time', drop=True)

df