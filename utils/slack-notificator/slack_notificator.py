import logging.config
from pathlib import Path
import requests
import json

logger_config_path = Path(__file__).parent.joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class SlackNotifier:

    def __init__(self, config='../../config/slack-config.json'):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.configFile = config
        self.hookURL = None
        self.__load_config()

    def __load_config(self):
        with open(self.configFile, 'r') as f:
            self.hookURL = json.load(f)['hookURL']

    def notify(self, message):
        try:
            response = requests.post(self.hookURL, json.dumps({"text": message}))
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.__logger.error("error when trying to send message", err)
        except requests.exceptions.ConnectionError as err:
            self.__logger.error("connection error occurred", err)
        except requests.exceptions.Timeout as err:
            self.__logger.error("timeout", err)
        except requests.exceptions.RequestException as err:
            self.__logger.error("request error", err)

        self.__logger.info("message sent: %s", message)
