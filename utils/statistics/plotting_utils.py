import matplotlib.pyplot as plt
import subprocess
import os
from pathlib import Path
from utils.imgur_uploader.imgur_uploader import ImgurUploader


class PlottingUtils:
    def __init__(self):
        self.uploaded_plots = dict()
        self.__uploader = ImgurUploader()
        self.__commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

    def create_plot(self, metric, metric_arr, val_metric_arr):
        plt.plot(metric_arr)
        plt.plot(val_metric_arr)
        plt.title(f'model {metric}')
        plt.ylabel(metric)
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')

        image_path = self.save_to_file(metric)
        uploaded_url = self.__uploader.upload_image(image_path)
        self.uploaded_plots[metric] = uploaded_url

        plt.clf()
        plt.cla()

    def save_to_file(self, metric):
        output_path = Path(__file__).parent.joinpath("outputs")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        commit_dir_path = Path(output_path).joinpath(self.__commit_hash)
        if not os.path.exists(commit_dir_path):
            os.mkdir(commit_dir_path)

        image_path = Path(__file__).parent \
            .joinpath("outputs") \
            .joinpath(f'{self.__commit_hash}') \
            .joinpath(f"{self.__commit_hash}_{metric}_plot.png")

        plt.savefig(image_path)

        return image_path
