import json
from random import randint
from channels.generic.websocket import WebsocketConsumer
from modbus import get_data
from database import *
from parameters import *
from display import *


class WSConsumer(WebsocketConsumer):  # subclass from WebsocketConsumer class
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.size_sqlite = 0
        self.size_csv = 0

        # delete old databases
        if path_csv.is_file():
            del_database(path_csv)
        if path_sqlite.is_file():
            del_database(path_sqlite)

        # Init Display
        self.miniDisplay = PiOLED()

    def connect(self):
        self.accept()

        # create new database with maxsize
        for i in range(10):
            dataRow = get_data()
            if (size_csv < max_Size) or (size_sqlite < max_Size):
                size_csv = store_data_csv(dataRow, path_csv)  # store to .csv
                size_sqlite = store_data_sqlite3(dataRow, path_sqlite)  # store to .sqlite
            else:
                print("Database is full: " + str(size_csv) + " Bytes")
                break
            if i < 1:
                self.miniDisplay.set_string("Messung läuft !")
        self.miniDisplay.set_string("Messung gestoppt !")

        # send data
        self.send(json.dumps({'VL1': randint(1, 100),
                              'VL2': randint(1, 10)}))

        # print
        print(dataRow)
