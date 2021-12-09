import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from pathlib import Path
import pandas as pd
import numpy as np

from .database import del_database, store_data_csv, store_data_sqlite3
from .display import PiOLED
from .modbus import get_data


class WSConsumer(WebsocketConsumer):  # subclass from WebsocketConsumer class
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_sqlite = 0
        self.size_csv = 0
        # database Param
        self.max_Size = 1000000  # max Size (Byte)
        self.path_csv = Path("./database/myData.csv")
        self.path_sqlite = Path("./database/myData.sqlite")
        # modbus Param
        self.dataRow = pd.DataFrame()

        # delete old databases
        if self.path_csv.is_file():
            del_database(self.path_csv)
        if self.path_sqlite.is_file():
            del_database(self.path_sqlite)

        # Init Display
        self.miniDisplay = PiOLED()
        self.miniDisplay.set_string("Start Log Data!")

    def connect(self):
        self.accept()

        i = 0
        # create new database with maxsize
        while 1:
            # get data from PRO380-Mod
            self.dataRow = get_data()
            # update database
            if (self.size_csv < self.max_Size) or (self.size_sqlite < self.max_Size):
                self.size_csv = store_data_csv(self.dataRow, self.path_csv)  # store to .csv
                self.size_sqlite = store_data_sqlite3(self.dataRow, self.path_sqlite)  # store to .sqlite
            else:
                if i == 0:
                    print("Database is full: " + str(self.size_csv) + " Bytes")
                    self.miniDisplay.set_string("Stop Log Data!")
                    i = 1
            # update webpage
            self.send(json.dumps({'VL1': float(self.dataRow["V_L1"]),
                                  'VL2': float(self.dataRow["V_L2"]),
                                  'VL3': float(self.dataRow["V_L3"]),
                                  'VMean': np.round((float(self.dataRow["V_L1"]) + float(self.dataRow["V_L2"]) + float(
                                      self.dataRow["V_L3"])) / 3, decimals=3),
                                  'IL1': float(self.dataRow["I_L1"]),
                                  'IL2': float(self.dataRow["I_L2"]),
                                  'IL3': float(self.dataRow["I_L3"]),
                                  'IMean': np.round((float(self.dataRow["I_L1"]) + float(self.dataRow["I_L2"]) + float(
                                      self.dataRow["I_L3"])) / 3, decimals=3),
                                  'PF1': float(self.dataRow["pf_L1"]),
                                  'PF2': float(self.dataRow["pf_L2"]),
                                  'PF3': float(self.dataRow["pf_L3"]),
                                  'PFMean': float(self.dataRow["pf"]),
                                  'p1': float(self.dataRow["p_L1"]),
                                  'p2': float(self.dataRow["p_L2"]),
                                  'p3': float(self.dataRow["p_L3"]),
                                  'pSum': float(self.dataRow["p_sum"]),
                                  'q1': float(self.dataRow["q_L1"]),
                                  'q2': float(self.dataRow["q_L2"]),
                                  'q3': float(self.dataRow["q_L3"]),
                                  'qSum': float(self.dataRow["q_sum"]),
                                  's1': float(self.dataRow["s_L1"]),
                                  's2': float(self.dataRow["s_L2"]),
                                  's3': float(self.dataRow["s_L3"]),
                                  'sSum': float(self.dataRow["s_sum"]),
                                  'eA1': float(self.dataRow["eAct_L1"]),
                                  'eA2': float(self.dataRow["eAct_L2"]),
                                  'eA3': float(self.dataRow["eAct_L3"]),
                                  'eASum': float(self.dataRow["eAct_Tot"]),
                                  'eR1': float(self.dataRow["eReact_L1"]),
                                  'eR2': float(self.dataRow["eReact_L2"]),
                                  'eR3': float(self.dataRow["eReact_L3"]),
                                  'eRSum': float(self.dataRow["eReact_Tot"]),
                                  'freq': float(self.dataRow["freq"]),
                                  }))