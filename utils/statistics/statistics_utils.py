from typing import List
from tensorflow.keras.callbacks import History
from utils.statistics.plotting_utils import PlottingUtils
from utils.statistics.statistic_metrics.statistic_metrics import Metric
import numpy as np


class StatisticsUtils:
    ROUND_DIGITS = 4

    def __init__(self, ml_model_results: List):
        self.__results: List[History] = ml_model_results
        self.__plotter = PlottingUtils()

    def calculate_all_statistics(self):
        calculated_statistics = dict()

        calculated_statistics[Metric.ACC] = self.get_mean_accuracy()
        calculated_statistics[Metric.LOSS] = self.get_mean_loss()
        calculated_statistics[Metric.FAR] = self.get_mean_false_acceptance_rate()
        calculated_statistics[Metric.FRR] = self.get_mean_false_rejection_rate()
        calculated_statistics[Metric.FN] = self.get_mean_false_negatives()
        calculated_statistics[Metric.FP] = self.get_mean_false_positives()
        calculated_statistics[Metric.TN] = self.get_mean_true_negatives()
        calculated_statistics[Metric.TP] = self.get_mean_true_positives()
        calculated_statistics[Metric.ACC_PLOT] = self.create_model_accuracy_training_plot()
        calculated_statistics[Metric.LOSS_PLOT] = self.create_model_loss_training_plot()
        calculated_statistics[Metric.PERCENTILES_HISTOGRAM] = self.create_model_accuracy_percentile_histogram()

        self.__plotter.save_plotted_data_to_csv()

        return calculated_statistics

    def create_model_accuracy_training_plot(self):
        return self.__create_model_training_plot(Metric.ACC)

    def create_model_loss_training_plot(self):
        return self.__create_model_training_plot(Metric.LOSS)

    def __create_model_training_plot(self, metric):
        results_matrix = [record.history[metric] for record in self.__results]
        val_results_matrix = [record.history[f'val_{metric}'] for record in self.__results]

        mean_epoch_values = np.mean(results_matrix, axis=0).round(StatisticsUtils.ROUND_DIGITS)
        mean_epoch_values = StatisticsUtils.to_percentage(mean_epoch_values)
        mean_val_epoch_values = np.mean(val_results_matrix, axis=0).round(StatisticsUtils.ROUND_DIGITS)
        mean_val_epoch_values = StatisticsUtils.to_percentage(mean_epoch_values)

        return self.__plotter.create_plot(metric, mean_epoch_values, mean_val_epoch_values)

    def create_model_accuracy_percentile_histogram(self):
        acc_results = [record.history[Metric.ACC][-1] for record in self.__results]
        acc_results = np.round(acc_results, StatisticsUtils.ROUND_DIGITS)
        acc_results = StatisticsUtils.to_percentage(acc_results)
        acc_results.sort()
        return self.__plotter.create_histogram(acc_results)

    def get_mean_accuracy(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_for_metric(Metric.ACC))

    def get_mean_loss(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_for_metric(Metric.LOSS))

    def __calculate_mean_for_metric(self, metric):
        final_values = [record.history[metric][-1] for record in self.__results]
        final_values_mean = np.mean(final_values).round(StatisticsUtils.ROUND_DIGITS)
        return final_values_mean

    def get_mean_false_negatives(self):
        return self.__calculate_mean_from_confusion_matrix(Metric.FN)

    def get_mean_false_positives(self):
        return self.__calculate_mean_from_confusion_matrix(Metric.FP)

    def get_mean_true_negatives(self):
        return self.__calculate_mean_from_confusion_matrix(Metric.TN)

    def get_mean_true_positives(self):
        return self.__calculate_mean_from_confusion_matrix(Metric.TP)

    def __calculate_mean_from_confusion_matrix(self, metric):
        values = [record.history[metric][-1] for record in self.__results]
        return np.mean(values).astype(int)

    def get_mean_false_rejection_rate(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_rate_from_confusion_matrix(Metric.FN, Metric.TP))

    def get_mean_false_acceptance_rate(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_rate_from_confusion_matrix(Metric.FP, Metric.TN))

    def __calculate_mean_rate_from_confusion_matrix(self, metric1, metric2):
        single_rate_list = [record.history[metric1][-1] / (record.history[metric1][-1] + record.history[metric2][-1])
                            for record in self.__results]
        return np.mean(single_rate_list).round(StatisticsUtils.ROUND_DIGITS)

    @staticmethod
    def to_percentage(value):
        return value * 100
