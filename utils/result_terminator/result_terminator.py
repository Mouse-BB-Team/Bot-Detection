import json
from pathlib import Path
import logging.config
from filelock import FileLock
from typing import Dict, List
import csv
import os
from utils.slack_notifier import *

logger_config_path = Path(__file__).parent.joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class ResultTerminator:

    def __init__(self, field_list: List[str], config='../../config/output-config.json'):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.configFile = config
        self.outputPath = None
        self.schema = field_list
        self.slack_notifier = SlackNotifier()
        self.__load_config()

    def __load_config(self):
        with open(self.configFile, 'r') as f:
            self.outputPath = json.load(f)['outputPath']

    def __create_file(self):
        with FileLock(self.outputPath + '.lock'):
            with open(self.outputPath, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.schema)
                writer.writeheader()

    def __append_file(self, element: Dict[str, str]):
        with FileLock(self.outputPath + '.lock'):
            with open(self.outputPath, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=self.schema)
                writer.writerow(element)

    def terminate(self, data, message):
        if not os.path.isfile(self.outputPath):
            self.__create_file()
        self.__append_file(data)
        self.slack_notifier.notify(message)
