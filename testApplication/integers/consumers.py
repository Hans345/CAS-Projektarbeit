import json
import time
from random import randint
from channels.generic.websocket import WebsocketConsumer
from pathlib import Path
import pandas as pd

from .database import del_database, store_data_csv, store_data_sqlite3
from .display import PiOLED
from .modbus import get_data


class WSConsumer(WebsocketConsumer):  # subclass from WebsocketConsumer class
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_sqlite = 0
        self.size_csv = 0
        # database Param
        self.max_Size = 1000  # max Size (Byte)
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

    def connect(self):
        self.accept()

        # create new database with maxsize
        for i in range(10):
            self.dataRow = get_data()
            if (self.size_csv < self.max_Size) or (self.size_sqlite < self.max_Size):
                self.size_csv = store_data_csv(self.dataRow, self.path_csv)  # store to .csv
                self.size_sqlite = store_data_sqlite3(self.dataRow, self.path_sqlite)  # store to .sqlite
            else:
                print("Database is full: " + str(self.size_csv) + " Bytes")
                break
            if i < 1:
                self.miniDisplay.set_string("Messung läuft !")
            # send data
            self.send(json.dumps({'VL1': float(self.dataRow["V_L1"]),
                                  'VL2': float(self.dataRow["V_L2"]),
                                  'VL3': float(self.dataRow["V_L3"]),
                                  }))
        self.miniDisplay.set_string("Messung gestoppt !")

        # print
        print(self.dataRow)
