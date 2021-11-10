from pathlib import Path

my_file = Path("database/myData.csv")


def store_data(data):
    if my_file.is_file():
        data.to_csv(path_or_buf=my_file)
    else:
        data.to_csv(path_or_buf=my_file, header=False, mode='a')
