import logging.config
from pathlib import Path
import requests
import json

logger_config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class SlackNotifier:

    def __init__(self, config='../../config/slack-config.json'):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__config_file = config
        self.__hook_URL = None
        self.__load_config()

    def __load_config(self):
        with open(self.__config_file, 'r') as f:
            self.__hook_URL = json.load(f)['hookURL']

    def notify(self, json_message):
        try:
            message = json.dumps(json_message)
            response = requests.post(self.__hook_URL, message)
            response.raise_for_status()
            self.__logger.info("message sent")
        except requests.exceptions.HTTPError as err:
            self.__logger.error("error when trying to send message", err)
        except requests.exceptions.ConnectionError as err:
            self.__logger.error("connection error occurred", err)
        except requests.exceptions.Timeout as err:
            self.__logger.error("timeout", err)
        except requests.exceptions.RequestException as err:
            self.__logger.error("request error", err)
