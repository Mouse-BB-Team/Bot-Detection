from typing import List, AnyStr
from tensorflow.keras.callbacks import History
from utils.statistics.plotting_utils import PlottingUtils
import numpy as np


FP = 'false_positives'
FN = 'false_negatives'
TN = 'true_negatives'
TP = 'true_positives'


class StatisticsUtils:
    def __init__(self, ml_model_results: List):
        self.__results: List[History] = ml_model_results
        self.__available_metrics: List[AnyStr] = self.__results[0].history.keys()
        self.plotter = PlottingUtils()

    def calculate_all_statistics(self):
        calculated_statistics = dict()
        calculated_statistics['accuracy'] = self.get_mean_accuracy()
        calculated_statistics['loss'] = self.get_mean_loss()
        calculated_statistics['far'] = self.get_mean_false_acceptance_rate()
        calculated_statistics['frr'] = self.get_mean_false_rejection_rate()
        calculated_statistics[FN] = self.get_mean_false_negatives()
        calculated_statistics[FP] = self.get_mean_false_positives()
        calculated_statistics[TN] = self.get_mean_true_negatives()
        calculated_statistics[TP] = self.get_mean_true_positives()
        return calculated_statistics

    def create_model_accuracy_training_plot(self):
        return self.__create_model_training_plot("accuracy")

    def create_model_loss_training_plot(self):
        return self.__create_model_training_plot("loss")

    def __create_model_training_plot(self, metric):
        results_matrix = [record.history[metric] for record in self.__results]
        val_results_matrix = [record.history[f'val_{metric}'] for record in self.__results]

        mean_epoch_values = np.mean(results_matrix, axis=0)
        mean_val_epoch_values = np.mean(val_results_matrix, axis=0)

        return self.plotter.create_plot(metric, mean_epoch_values, mean_val_epoch_values)

    # TODO
    def create_model_accuracy_percentile_histogram(self):
        acc_results = [round(record.history['accuracy'][-1], 2) for record in self.__results]
        percentiles = [np.percentile(acc_results, i) for i in range(1, 101, 5)]
        self.plotter.create_histogram(percentiles)

    def get_mean_accuracy(self):
        return self.__calculate_mean_for_metric("accuracy")

    def get_mean_loss(self):
        return self.__calculate_mean_for_metric("loss")

    def __calculate_mean_for_metric(self, metric):
        final_values = [record.history[metric][-1] for record in self.__results]
        final_values_mean = np.mean(final_values)
        return final_values_mean

    def get_mean_false_negatives(self):
        return self.__calculate_mean_from_confusion_matrix(FN)

    def get_mean_false_positives(self):
        return self.__calculate_mean_from_confusion_matrix(FP)

    def get_mean_true_negatives(self):
        return self.__calculate_mean_from_confusion_matrix(TN)

    def get_mean_true_positives(self):
        return self.__calculate_mean_from_confusion_matrix(TP)

    def __calculate_mean_from_confusion_matrix(self, metric):
        values = [record.history[metric] for record in self.__results]
        return np.mean(values)

    def get_mean_false_rejection_rate(self):
        return self.__calculate_mean_rate_from_confusion_matrix(FN, TP)

    def get_mean_false_acceptance_rate(self):
        return self.__calculate_mean_rate_from_confusion_matrix(FP, TN)

    def __calculate_mean_rate_from_confusion_matrix(self, metric_1, metric_2):
        confusion_matrix = {}
        single_rate_list = []
        for record in self.__results:
            for metric in [FN, FP, TN, TP]:
                confusion_matrix[metric] = record.history[metric]
            single_rate = confusion_matrix[metric_1] / (confusion_matrix[metric_1] + confusion_matrix[metric_2])
            single_rate_list.append(single_rate)
        return np.mean(single_rate_list)
