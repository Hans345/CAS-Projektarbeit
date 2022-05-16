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
        self.max_Size = 1048576  # max Size (Byte)
        self.path_csv = Path("./database/myData.csv")
        self.path_sqlite = Path("./database/myData.sqlite")
        # modbus Param
        self.dataRow_pruefstandLinks = pd.DataFrame()

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
        for i in range(100):  # after 100 measurements --> WebSocket DISCONNECT
            # get data from PRO380-Mod: Prüfstand Links
            self.dataRow_pruefstandLinks = get_data(port='/dev/ttyUSB0', adr=1)
            # update database only Pruefstand Links!
            if (self.size_csv < self.max_Size) or (self.size_sqlite < self.max_Size):
                self.size_csv = store_data_csv(self.dataRow_pruefstandLinks, self.path_csv)  # store to .csv
                self.size_sqlite = store_data_sqlite3(self.dataRow_pruefstandLinks, self.path_sqlite)  # store to .sqlite
            else:
                if i == 0:
                    print("Database is full: " + str(self.size_csv) + " Bytes")
                    self.miniDisplay.set_string("Stop Log Data!")
                    i = 1
            # update webpage: Prüfstand Links
            self.send(json.dumps({'VL1': float(self.dataRow_pruefstandLinks["V_L1"]),
                                  'VL2': float(self.dataRow_pruefstandLinks["V_L2"]),
                                  'VL3': float(self.dataRow_pruefstandLinks["V_L3"]),
                                  'VMean': np.round((float(self.dataRow_pruefstandLinks["V_L1"]) + float(self.dataRow_pruefstandLinks["V_L2"]) + float(
                                      self.dataRow_pruefstandLinks["V_L3"])) / 3, decimals=3),
                                  'IL1': float(self.dataRow_pruefstandLinks["I_L1"]),
                                  'IL2': float(self.dataRow_pruefstandLinks["I_L2"]),
                                  'IL3': float(self.dataRow_pruefstandLinks["I_L3"]),
                                  'IMean': np.round((float(self.dataRow_pruefstandLinks["I_L1"]) + float(self.dataRow_pruefstandLinks["I_L2"]) + float(
                                      self.dataRow_pruefstandLinks["I_L3"])) / 3, decimals=3),
                                  'PF1': float(self.dataRow_pruefstandLinks["pf_L1"]),
                                  'PF2': float(self.dataRow_pruefstandLinks["pf_L2"]),
                                  'PF3': float(self.dataRow_pruefstandLinks["pf_L3"]),
                                  'PFMean': float(self.dataRow_pruefstandLinks["pf"]),
                                  'p1': float(self.dataRow_pruefstandLinks["p_L1"]),
                                  'p2': float(self.dataRow_pruefstandLinks["p_L2"]),
                                  'p3': float(self.dataRow_pruefstandLinks["p_L3"]),
                                  'pSum': float(self.dataRow_pruefstandLinks["p_sum"]),
                                  'q1': float(self.dataRow_pruefstandLinks["q_L1"]),
                                  'q2': float(self.dataRow_pruefstandLinks["q_L2"]),
                                  'q3': float(self.dataRow_pruefstandLinks["q_L3"]),
                                  'qSum': float(self.dataRow_pruefstandLinks["q_sum"]),
                                  's1': float(self.dataRow_pruefstandLinks["s_L1"]),
                                  's2': float(self.dataRow_pruefstandLinks["s_L2"]),
                                  's3': float(self.dataRow_pruefstandLinks["s_L3"]),
                                  'sSum': float(self.dataRow_pruefstandLinks["s_sum"]),
                                  'eA1': float(self.dataRow_pruefstandLinks["eAct_L1"]),
                                  'eA2': float(self.dataRow_pruefstandLinks["eAct_L2"]),
                                  'eA3': float(self.dataRow_pruefstandLinks["eAct_L3"]),
                                  'eASum': float(self.dataRow_pruefstandLinks["eAct_Tot"]),
                                  'eR1': float(self.dataRow_pruefstandLinks["eReact_L1"]),
                                  'eR2': float(self.dataRow_pruefstandLinks["eReact_L2"]),
                                  'eR3': float(self.dataRow_pruefstandLinks["eReact_L3"]),
                                  'eRSum': float(self.dataRow_pruefstandLinks["eReact_Tot"]),
                                  'freq': float(self.dataRow_pruefstandLinks["freq"]),
                                  }))

            # TODO: check Port
            # update webpage: Pruefstand Ecke
            self.dataRow_pruefstandEcke = get_data(port='/dev/ttyUSB1', adr=2)
            self.send(json.dumps({'VL1_e': float(self.dataRow_pruefstandEcke["V_L1"]),
                                  'VL2_e': float(self.dataRow_pruefstandEcke["V_L2"]),
                                  'VL3_e': float(self.dataRow_pruefstandEcke["V_L3"]),
                                  'VMean_e': np.round((float(self.dataRow_pruefstandEcke["V_L1"]) + float(self.dataRow_pruefstandEcke["V_L2"]) + float(
                                      self.dataRow_pruefstandEcke["V_L3"])) / 3, decimals=3),
                                  'IL1_e': float(self.dataRow_pruefstandEcke["I_L1"]),
                                  'IL2_e': float(self.dataRow_pruefstandEcke["I_L2"]),
                                  'IL3_e': float(self.dataRow_pruefstandEcke["I_L3"]),
                                  'IMean_e': np.round((float(self.dataRow_pruefstandEcke["I_L1"]) + float(self.dataRow_pruefstandEcke["I_L2"]) + float(
                                      self.dataRow_pruefstandEcke["I_L3"])) / 3, decimals=3),
                                  'PF1_e': float(self.dataRow_pruefstandEcke["pf_L1"]),
                                  'PF2_e': float(self.dataRow_pruefstandEcke["pf_L2"]),
                                  'PF3_e': float(self.dataRow_pruefstandEcke["pf_L3"]),
                                  'PFMean_e': float(self.dataRow_pruefstandEcke["pf"]),
                                  'p1_e': float(self.dataRow_pruefstandEcke["p_L1"]),
                                  'p2_e': float(self.dataRow_pruefstandEcke["p_L2"]),
                                  'p3_e': float(self.dataRow_pruefstandEcke["p_L3"]),
                                  'pSum_e': float(self.dataRow_pruefstandEcke["p_sum"]),
                                  'q1_e': float(self.dataRow_pruefstandEcke["q_L1"]),
                                  'q2_e': float(self.dataRow_pruefstandEcke["q_L2"]),
                                  'q3_e': float(self.dataRow_pruefstandEcke["q_L3"]),
                                  'qSum_e': float(self.dataRow_pruefstandEcke["q_sum"]),
                                  's1_e': float(self.dataRow_pruefstandEcke["s_L1"]),
                                  's2_e': float(self.dataRow_pruefstandEcke["s_L2"]),
                                  's3_e': float(self.dataRow_pruefstandEcke["s_L3"]),
                                  'sSum_e': float(self.dataRow_pruefstandEcke["s_sum"]),
                                  'eA1_e': float(self.dataRow_pruefstandEcke["eAct_L1"]),
                                  'eA2_e': float(self.dataRow_pruefstandEcke["eAct_L2"]),
                                  'eA3_e': float(self.dataRow_pruefstandEcke["eAct_L3"]),
                                  'eASum_e': float(self.dataRow_pruefstandEcke["eAct_Tot"]),
                                  'eR1_e': float(self.dataRow_pruefstandEcke["eReact_L1"]),
                                  'eR2_e': float(self.dataRow_pruefstandEcke["eReact_L2"]),
                                  'eR3_e': float(self.dataRow_pruefstandEcke["eReact_L3"]),
                                  'eRSum_e': float(self.dataRow_pruefstandEcke["eReact_Tot"]),
                                  'freq_e': float(self.dataRow_pruefstandEcke["freq"]),
                                  }))
            # TODO
            # Webseite wird geschlossen: while Schleife mittels break verlassen
            # Server wird beendet (Terminal: Ctrl +C), while-Schleife soll ebenfalls mit break verlassen werden.