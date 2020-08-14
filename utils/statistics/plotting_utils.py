import matplotlib.pyplot as plt
import subprocess
import os
import csv
from pathlib import Path
from utils.imgur_uploader.imgur_uploader import ImgurUploader
import numpy as np
from itertools import zip_longest


class PlottingUtils:
    def __init__(self):
        self.__plotted_data = dict()
        self.__uploader = ImgurUploader()
        self.__commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        # TODO: on prometheus save outputs on shared team space
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

    def create_histogram(self, values_arr):
        percentiles = [x for x in range(5, 100, 5)]
        percentiles.append(99)

        percentiles_values = np.percentile(values_arr, percentiles)

        percentiles_values_round = percentiles_values.astype(int)

        bars = plt.bar(percentiles, percentiles_values_round, width=2.4, align='edge', tick_label=percentiles)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, yval)

        plt.title(f'model accuracy percentiles histogram')
        plt.ylabel("Accuracy [%]")
        plt.xlabel('Percentile')

        image_path = self.__save_image("percentile")
        uploaded_url = self.__uploader.upload_image(image_path)
        self.__plotted_data["perc_accuracy_val"] = percentiles_values
        self.__plotted_data["percentiles"] = percentiles

        plt.clf()
        plt.cla()

        return uploaded_url

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
            rows = zip_longest(*data)
            for row in rows:
                writer.writerow(row)
