from pathlib import Path

my_dir = Path("./database/")
my_file = Path("./database/myData.csv")
max_Size = 400


###############################################################################
def store_data(data):
    size = 0
    if my_dir.is_dir():
        if my_file.is_file():
            size = my_file.stat().st_size
            if size < max_Size:  # check Size Database
                data.to_csv(path_or_buf=my_file, header=False, mode='a')
        else:
            data.to_csv(path_or_buf=my_file)
    else:
        my_dir.mkdir()
        data.to_csv(path_or_buf=my_file)

    return size


###############################################################################
def del_database():
    my_file.unlink()
