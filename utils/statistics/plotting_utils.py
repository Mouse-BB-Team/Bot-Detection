import matplotlib.pyplot as plt
import subprocess
import os
import csv
from pathlib import Path
from utils.imgur_uploader.imgur_uploader import ImgurUploader
import numpy as np


class PlottingUtils:
    def __init__(self):
        self.__plotted_data = dict()
        self.__uploader = ImgurUploader()
        self.__commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        self.__output_dir_path = Path(__file__).parent.joinpath("outputs")
        self.__commit_dir_path = Path(self.__output_dir_path).joinpath(self.__commit_hash)

    def create_plot(self, metric_name, metric_arr, val_metric_arr):
        plt.plot(metric_arr)
        plt.plot(val_metric_arr)

        plt.title(f'model {metric_name}')
        plt.ylabel(metric_name)
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')

        image_path = self.__save_image(metric_name)
        uploaded_url = self.__uploader.upload_image(image_path)

        self.__plotted_data[metric_name] = metric_arr
        self.__plotted_data[f'val_{metric_name}'] = val_metric_arr

        plt.clf()
        plt.cla()

        return uploaded_url

    # TODO
    def create_histogram(self, values_arr):
        percentiles = [10, 20, 30, 50, 75, 90, 100]
        percentiles_values = np.percentile(values_arr, percentiles)
        plt.show()

    def __save_image(self, metric_name):
        if not os.path.exists(self.__output_dir_path):
            os.mkdir(self.__output_dir_path)
        if not os.path.exists(self.__commit_dir_path):
            os.mkdir(self.__commit_dir_path)

        image_path = self.__commit_dir_path.joinpath(f"{self.__commit_hash}_{metric_name}_plot.png")

        plt.savefig(image_path)

        return image_path

    def save_plotted_data_to_csv(self):
        csv_path = self.__commit_dir_path.joinpath(f"{self.__commit_hash}_data.csv")
        keys = self.__plotted_data.keys()
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(keys)
            data = (self.__plotted_data[key] for key in keys)
            rows = zip(*data)
            for row in rows:
                writer.writerow(row)
