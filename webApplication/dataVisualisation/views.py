from django.shortcuts import render
from django.http import HttpResponse
from . import modbus
from . import database
from . import parameters
from . import display

#####################################################################################
from .database import del_database, store_data_csv, store_data_sqlite3
from .modbus import get_data
from .parameters import path_csv, path_sqlite, max_Size, data, dataRow


def test(request):
    """
    :param request: Anfrage
    :return:
    """
    # Display
    size_csv = 0
    size_sqlite = 0

    # delete old databases
    if path_csv.is_file():
        del_database(path_csv)
    if path_sqlite.is_file():
        del_database(path_sqlite)

    # Display
    miniDisplay = display.PiOLED()

    # create new database with maxsize
    for i in range(10):
        if (size_csv < max_Size) or (size_sqlite < max_Size):
            dataRow = get_data()
            data = data.append(dataRow)
            size_csv = store_data_csv(dataRow, path_csv)  # store to .csv
            size_sqlite = store_data_sqlite3(dataRow, path_sqlite)  # store to .sqlite
        else:
            print("Database is full: " + str(size_csv) + " Bytes")
            break
        if i < 1:
            miniDisplay.set_string("Messung läuft !")
    miniDisplay.set_string("Init Done !")

    print(data.head())

    return HttpResponse("Test Done!")
