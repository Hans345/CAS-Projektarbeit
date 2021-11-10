"""
Store Data to .csv
@author: Raphael Baumeler/2021
"""
###############################################################################
def store_data(data_row, dir_path, dir_file):
    size = 0
    if dir_path.is_dir():
        if dir_file.is_file():
            size = dir_file.stat().st_size
            data_row.to_csv(path_or_buf=dir_file, header=False, mode='a')
        else:
            data_row.to_csv(path_or_buf=dir_file)
    else:
        dir_path.mkdir()
        data_row.to_csv(path_or_buf=dir_file)

    return size


###############################################################################
def del_database(dir_file):
    dir_file.unlink()
