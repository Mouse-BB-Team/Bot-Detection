from typing import List, AnyStr
from tensorflow.keras.callbacks import History
from utils.statistics.plotting_utils import PlottingUtils
import numpy as np
import re


# TODO 3 obrazki acc loss i percentyle po accuracy
# TODO liczbowe metryki confusion matrix + FPR + FNR czy jakoś tak
# TODO percentile po accuracy, FAR + to drugie
# TODO plotly with http - loss + accuracy
# TODO acc i loss uśrednianie po indeksie (średnie z ostatnich epok)
# TODO Save to csv


class StatisticsUtils:
    def __init__(self, ml_model_results: List):
        self.__results: List[History] = ml_model_results
        self.__available_metrics: List[AnyStr] = self.__results[0].history.keys()
        self.calculated_statistics = dict()
        self.plotter = PlottingUtils()
        self.__calculate_statistics()

    def __calculate_statistics(self):
        for metric in self.__available_metrics:
            self.calculate_mean_for_metric(metric)
            self.calculate_std_for_metric(metric)

    def create_final_mean_accuracy_plot(self):
        acc_results_matrix = [record.history['accuracy'] for record in self.__results]
        val_acc_results_matrix = [record.history['val_accuracy'] for record in self.__results]

        mean_acc_epoch_values = np.mean(acc_results_matrix, axis=0)
        mean_val_acc_epoch_values = np.mean(val_acc_results_matrix, axis=0)

        self.plotter.create_plot("accuracy", mean_acc_epoch_values, mean_val_acc_epoch_values)

    def create_final_mean_loss_plot(self):
        loss_results_matrix = [record.history['loss'] for record in self.__results]
        val_loss_results_matrix = [record.history['val_loss'] for record in self.__results]

        mean_loss_epoch_values = np.mean(loss_results_matrix, axis=0)
        mean_val_loss_epoch_values = np.mean(val_loss_results_matrix, axis=0)

        self.plotter.create_plot("loss", mean_loss_epoch_values, mean_val_loss_epoch_values)

    def calculate_mean_for_metric(self, metric_name):
        attribute_name = self.__find_metric_name(metric_name)

        mean_list = [np.mean(result.history[attribute_name]) for result in self.__results]
        global_mean = np.mean(mean_list)

        self.calculated_statistics[f"{attribute_name}_mean"] = global_mean

        return global_mean

    def calculate_std_for_metric(self, metric, std_mean=True):
        attribute_name = self.__find_metric_name(metric)

        val_list = [result.history[metric] for result in self.__results]
        std_list = [np.std(val) if isinstance(val, list) else np.std(val_list) for val in val_list]

        global_std = np.mean(std_list) if std_mean else std_list

        self.calculated_statistics[f"{attribute_name}_std"] = global_std

        return global_std

    def __find_metric_name(self, metric):
        attribute_name = None
        for attribute in self.__available_metrics:
            if re.search(f"^{metric}*", attribute) is not None:
                attribute_name = attribute
                break

        if attribute_name is None:
            raise AttributeError(f"No {metric} metric attribute in history object.")

        return attribute_name