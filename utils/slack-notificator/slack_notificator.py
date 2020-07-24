import logging.config
from pathlib import Path
import requests
import json

logger_config_path = Path(__file__).parent.joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class SlackNotifier:

    def __init__(self, config='./config.json'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.configFile = config
        self.hookURL = None
        self.__load_config()

    def __load_config(self):
        with open(self.configFile, 'r') as f:
            self.hookURL = json.load(f)['hookURL']

    def notify(self, message):
        response = requests.post(self.hookURL, json.dumps({"text": message}))
        if response.status_code == 200:
            self.logger.info("message sent: %s", message)
        else:
            self.logger.error("error when trying to send message: %s - %s", response.reason, response.status_code)
