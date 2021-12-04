import pandas as pd
from pathlib import Path

# database Param
max_Size = 1000  # max Size (Byte)
path_csv = Path("./database/myData.csv")
path_sqlite = Path("./database/myData.sqlite")

# modbus Param
data = pd.DataFrame()
dataRow = pd.DataFrame()