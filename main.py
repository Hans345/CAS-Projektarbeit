import datetime as dt
from modbus import get_data

t0 = dt.datetime.now()
print("Final DataRow: \n" + str(get_data()))
t1 = dt.datetime.now()
print('Time for reading: ' + str(t1 - t0))
