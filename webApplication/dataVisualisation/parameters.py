import pandas as pd
from pathlib import Path

# database Param
max_Size = 1000  # max Size (Byte)
path_csv = Path("C:/CAS_EnD_HS21/06_Projektarbeit/02_Code/database/myData.csv")
path_sqlite = Path("C:/CAS_EnD_HS21/06_Projektarbeit/02_Code/database/myData.sqlite")

# modbus Param
data = pd.DataFrame()
dataRow = pd.DataFrame()