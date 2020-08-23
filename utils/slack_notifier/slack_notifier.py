import logging.config
from pathlib import Path
import json
from http.client import HTTPSConnection

logger_config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('logger.config').absolute()
logging.config.fileConfig(logger_config_path)


class SlackNotifier:
    __config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('slack-config.json')

    def __init__(self, config=__config_path):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__config_file = config
        self.__hook_URL = None
        self.__hook_context = None
        self.__load_config()

    def __load_config(self):
        with open(self.__config_file, 'r') as f:
            loaded_config = json.load(f)
            self.__hook_URL = loaded_config['hookURL']
            self.__hook_context = loaded_config['hookContext']

    def notify(self, json_message):
        message = json.dumps(json_message)
        self.__http_post_request(message)

    def __http_post_request(self, json_msg):
        try:
            headers = {"Content-type": "application/json"}
            connection = HTTPSConnection(self.__hook_URL)
            connection.request("POST", self.__hook_context, json_msg, headers)
            response = connection.getresponse()
            if response.status != 200:
                raise AttributeError(f"Response body: {response.read()}")
        except Exception as e:
            raise e
        finally:
            connection.close()
