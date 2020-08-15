import matplotlib.pyplot as plt
import subprocess
import os
from pathlib import Path
from utils.imgur_uploader.imgur_uploader import ImgurUploader
import numpy as np
from utils.statistics.csv_writer.csv_writer import CSVWriter


class PlottingUtils:
    GROUP_NAME = 'plggpchdyplo'

    def __init__(self):
        self.__uploader = ImgurUploader()
        self.__commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        self.__group_storage_dir = Path(os.environ['PLG_GROUPS_STORAGE']).joinpath(PlottingUtils.GROUP_NAME)
        self.__output_dir_path = self.__group_storage_dir.joinpath("outputs")
        self.__commit_dir_path = self.__output_dir_path.joinpath(self.__commit_hash)
        self.csv_writer = CSVWriter()

    def create_plot(self, metric_name, metric_arr, val_metric_arr):
        plt.plot(metric_arr)
        plt.plot(val_metric_arr)

        plt.title(f'model {metric_name} [%]')
        plt.ylabel(metric_name)
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')

        self.csv_writer.append_data_to_csv([metric_name, f'val_{metric_name}'], metric_arr, val_metric_arr)

        image_path = self.__save_image(metric_name)
        uploaded_url = self.__uploader.upload_image(image_path)

        plt.clf()
        plt.cla()

        return uploaded_url

    def create_histogram(self, values_arr):
        percentiles = self.__get_percentiles()

        percentiles_values = np.percentile(values_arr, percentiles)

        percentiles_values_round = percentiles_values.astype(int)

        bars = plt.bar(percentiles, percentiles_values_round, width=2.4, align='edge', tick_label=percentiles)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, yval)

        plt.title(f'model accuracy percentiles histogram')
        plt.ylabel("Accuracy [%]")
        plt.xlabel('Percentile')

        self.csv_writer.append_data_to_csv(["percentiles_acc_val", "percentiles"], percentiles_values, percentiles)

        image_path = self.__save_image("percentile")
        uploaded_url = self.__uploader.upload_image(image_path)

        plt.clf()
        plt.cla()

        return uploaded_url

    def __get_percentiles(self):
        percentiles = [x for x in range(5, 100, 5)]
        percentiles.append(99)
        return percentiles

    def __save_image(self, metric_name):
        if not os.path.exists(self.__output_dir_path):
            os.mkdir(self.__output_dir_path)
        if not os.path.exists(self.__commit_dir_path):
            os.mkdir(self.__commit_dir_path)

        image_path = self.__commit_dir_path.joinpath(f"{self.__commit_hash}_{metric_name}_plot.png")

        plt.savefig(image_path)

        return image_path
