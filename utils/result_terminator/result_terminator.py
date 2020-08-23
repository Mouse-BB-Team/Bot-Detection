from pathlib import Path
import logging.config
from filelock import FileLock
from typing import Dict, List, AnyStr
import csv
import os

logger_config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)

LOCK_FILE_EXTENSION = '.lock'


class ResultTerminator:

    def __init__(self, field_list: List[str]):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__output_path = Path(os.environ['RESULTS_PATH']).joinpath("output.csv").absolute()
        self.__schema = field_list

    def __create_file(self):
        with FileLock(self.__output_path.__str__() + LOCK_FILE_EXTENSION):
            with open(self.__output_path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.__schema)
                writer.writeheader()

    def __append_file(self, element: Dict[AnyStr, AnyStr]):
        with FileLock(self.__output_path.__str__() + LOCK_FILE_EXTENSION):
            with open(self.__output_path, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=self.__schema)
                writer.writerow(element)

    def terminate(self, element: Dict[AnyStr, AnyStr]):
        if not os.path.isfile(self.__output_path):
            self.__create_file()
        self.__append_file(element)
