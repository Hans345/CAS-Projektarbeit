from pathlib import Path


def store_data(data):
    my_dir = Path("./database/")
    my_file = Path("./database/myData.csv")
    max_Size = 400  # 100 * 10 ** 6  # 100 MB

    size = my_file.stat().st_size
    if size < max_Size:
        if my_dir.is_dir():
            if my_file.is_file():
                data.to_csv(path_or_buf=my_file, header=False, mode='a')
            else:
                data.to_csv(path_or_buf=my_file)
        else:
            my_dir.mkdir()
            if my_file.is_file():
                data.to_csv(path_or_buf=my_file, header=False, mode='a')
            else:
                data.to_csv(path_or_buf=my_file)
        print("Database not Full")
    else:
        print("Database is Full")
