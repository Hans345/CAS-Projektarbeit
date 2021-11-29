"""
Store Data to .csv and to .sqlite
@author: Raphael Baumeler/2021
"""

###############################################################################
import sqlite3


###############################################################################
def store_data_csv(data_row, path):
    size = 0
    if path.parent.is_dir():
        if path.is_file():
            size = path.stat().st_size
            data_row.to_csv(path_or_buf=path, header=False, mode='a')
        else:
            data_row.to_csv(path_or_buf=path)
    else:
        path.parent.mkdir()
        data_row.to_csv(path_or_buf=path)

    return size


###############################################################################
def store_data_sqlite3(data_row, path):
    size = 0
    if path.parent.is_dir():
        if path.is_file():
            size = path.stat().st_size
            conn = sqlite3.connect(path)
            filename = path.name
            data_row.to_sql(filename, conn, if_exists='append', index=True)
        else:
            conn = sqlite3.connect(path)
            filename = path.name
            data_row.to_sql(filename, conn, if_exists='replace', index=True)
    else:
        path.parent.mkdir()
        conn = sqlite3.connect(path)
        filename = path.name
        data_row.to_sql(filename, conn, if_exists='replace', index=True)

    return size


###############################################################################
def del_database(path):
    path.unlink()
