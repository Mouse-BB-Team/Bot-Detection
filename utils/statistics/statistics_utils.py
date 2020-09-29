import subprocess
from typing import List, Dict
from utils.statistics.plotting_utils import PlottingUtils
from utils.statistics.statistic_metrics.statistic_metrics import Metric
from utils.result_terminator.result_terminator import ResultTerminator
import numpy as np


class StatisticsUtils:
    ROUND_DIGITS = 4

    def __init__(self, ml_model_results: List):
        self.__results: List[Dict] = ml_model_results
        self.__plotter = PlottingUtils()

    def calculate_all_statistics(self, terminate_to_csv=True):
        calculated_statistics = {Metric.ACC.value: self.get_mean_accuracy(),
                                 Metric.LOSS.value: self.get_mean_loss(),
                                 Metric.FAR.value: self.get_mean_false_acceptance_rate(),
                                 Metric.FRR.value: self.get_mean_false_rejection_rate(),
                                 Metric.FN.value: self.get_mean_false_negatives(),
                                 Metric.FP.value: self.get_mean_false_positives(),
                                 Metric.TN.value: self.get_mean_true_negatives(),
                                 Metric.TP.value: self.get_mean_true_positives(),
                                 Metric.ACC_PLOT.value: self.create_model_accuracy_training_plot(),
                                 Metric.LOSS_PLOT.value: self.create_model_loss_training_plot(),
                                 Metric.PERCENTILES_HISTOGRAM.value: self.create_model_accuracy_percentile_histogram()}

        if terminate_to_csv:
            self.__terminate_results(calculated_statistics)

        return calculated_statistics

    def __terminate_results(self, stat_dict):
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

        result_terminator_dict = {"commit_hash": commit_hash}
        result_terminator_dict.update(stat_dict)
        result_terminator_dict.pop(Metric.ACC_PLOT.value)
        result_terminator_dict.pop(Metric.LOSS_PLOT.value)
        result_terminator_dict.pop(Metric.PERCENTILES_HISTOGRAM.value)

        terminator = ResultTerminator([*result_terminator_dict.keys()])
        terminator.terminate(result_terminator_dict)

    def create_model_accuracy_training_plot(self):
        return self.__create_model_training_plot(Metric.ACC)

    def create_model_loss_training_plot(self):
        return self.__create_model_training_plot(Metric.LOSS)

    def __create_model_training_plot(self, metric: Metric):
        results_matrix = [record[metric.value] for record in self.__results]
        val_results_matrix = [record[f'val_{metric.value}'] for record in self.__results]

        mean_epoch_values = np.mean(results_matrix, axis=0).round(StatisticsUtils.ROUND_DIGITS)
        mean_epoch_values = StatisticsUtils.to_percentage(mean_epoch_values)
        mean_val_epoch_values = np.mean(val_results_matrix, axis=0).round(StatisticsUtils.ROUND_DIGITS)
        mean_val_epoch_values = StatisticsUtils.to_percentage(mean_val_epoch_values)

        return self.__plotter.create_plot(metric.value, mean_epoch_values, mean_val_epoch_values)

    def create_model_accuracy_percentile_histogram(self):
        acc_results = [record[f"val_{Metric.ACC.value}"][-1] for record in self.__results]
        acc_results = np.round(acc_results, StatisticsUtils.ROUND_DIGITS)
        acc_results = StatisticsUtils.to_percentage(acc_results)
        acc_results.sort()
        return self.__plotter.create_histogram(acc_results)

    def get_mean_accuracy(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_for_metric(Metric.ACC))

    def get_mean_loss(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_for_metric(Metric.LOSS))

    def __calculate_mean_for_metric(self, metric: Metric):
        final_values = [record[f"val_{metric.value}"][-1] for record in self.__results]
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

    def __calculate_mean_from_confusion_matrix(self, metric: Metric):
        values = [record[f"val_{metric.value}"][-1] for record in self.__results]
        return np.mean(values).astype(int)

    def get_mean_false_rejection_rate(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_rate_from_confusion_matrix(Metric.FN, Metric.TP))

    def get_mean_false_acceptance_rate(self):
        return StatisticsUtils.to_percentage(self.__calculate_mean_rate_from_confusion_matrix(Metric.FP, Metric.TN))

    def __calculate_mean_rate_from_confusion_matrix(self, metric1: Metric, metric2: Metric):
        single_rate_list = [record[f"val_{metric1.value}"][-1] /
                            (record[f"val_{metric1.value}"][-1] + record[f"val_{metric2.value}"][-1])
                            for record in self.__results]
        return np.mean(single_rate_list).round(StatisticsUtils.ROUND_DIGITS)

    @staticmethod
    def to_percentage(value):
        return value * 100
