from imgurpython import ImgurClient
from pathlib import Path
import json


class ImgurUploader:
    __config_path = Path(__file__).parent.parent.parent.joinpath('config').joinpath('imgur-config.json')

    def __init__(self, config_file_path=__config_path):
        self.__config_file = config_file_path
        self.__client_credentials: tuple = self.__load_config()
        self.__client = ImgurClient(*self.__client_credentials)

    def __load_config(self):
        with open(self.__config_file, 'r') as f:
            parsed_json = json.load(f)
            client_id = parsed_json['client_id']
            client_secret = parsed_json['client_secret']
        return client_id, client_secret

    def upload_image(self, image_path):
        uploaded_image = self.__client.upload_from_path(image_path)
        image_id = uploaded_image["id"]
        image_url = f"https://i.imgur.com/{image_id}.png"

        return image_url
