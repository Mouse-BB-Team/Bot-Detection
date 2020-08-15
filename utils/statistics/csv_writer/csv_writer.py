import csv
from itertools import zip_longest
from pathlib import Path
import subprocess
import os
import pandas as pd
from typing import List


class CSVWriter:
    GROUP_NAME = 'plggpchdyplo'

    def __init__(self):
        self.__commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        self.__group_storage_dir = Path(os.environ['PLG_GROUPS_STORAGE']).joinpath(CSVWriter.GROUP_NAME).absolute()
        self.__output_dir_path = self.__group_storage_dir.joinpath("outputs").absolute()
        self.__commit_dir_path = self.__output_dir_path.joinpath(self.__commit_hash).absolute()

    def append_data_to_csv(self, columns_names: List[str], *data, csv_out_path=None):
        csv_path = self.__check_csv_path(csv_out_path)

        if self.__is_csv_file_empty(csv_path):
            df = pd.read_csv(csv_path)

            if self.__is_column_already_in_file(df.keys(), columns_names):
                raise AttributeError("Key already exist in csv!")

            columns_names = [*df.keys(), *columns_names]
            old_data = [df[key] for key in df.keys()]
            data = [*old_data, *data]

        self.__save_data_to_csv(columns_names, data, csv_path)

    def __check_csv_path(self, csv_path):
        if csv_path is None:
            csv_path = self.__commit_dir_path.joinpath(f"{self.__commit_hash}_data.csv")
        if not os.path.exists(csv_path.parent):
            os.makedirs(csv_path.parent)
            open(csv_path, 'a').close()

        return csv_path

    def __is_csv_file_empty(self, csv_path):
        return os.stat(csv_path).st_size != 0

    def __is_column_already_in_file(self, column_names, columns_from_file):
        return len(set(column_names).intersection(set(columns_from_file)))

    def __save_data_to_csv(self, columns_names: List[str], *data, csv_path=None):
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(columns_names)
            rows = zip_longest(*data)
            for row in rows:
                writer.writerow(row)
