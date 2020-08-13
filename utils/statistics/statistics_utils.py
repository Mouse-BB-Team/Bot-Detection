from typing import List
from tensorflow.keras.callbacks import History
from utils.statistics.plotting_utils import PlottingUtils
import numpy as np

ACC = 'accuracy'
LOSS = 'loss'
FP = 'false_positives'
FN = 'false_negatives'
TN = 'true_negatives'
TP = 'true_positives'
FAR = 'false_acceptance_rate'
FRR = 'false_rejection_rate'


class StatisticsUtils:
    ROUND_DIGITS = 6

    def __init__(self, ml_model_results: List):
        self.__results: List[History] = ml_model_results
        self.plotter = PlottingUtils()

    def calculate_all_statistics(self):
        calculated_statistics = dict()

        calculated_statistics[ACC] = self.get_mean_accuracy()
        calculated_statistics[LOSS] = self.get_mean_loss()
        calculated_statistics[FAR] = self.get_mean_false_acceptance_rate()
        calculated_statistics[FRR] = self.get_mean_false_rejection_rate()
        calculated_statistics[FN] = self.get_mean_false_negatives()
        calculated_statistics[FP] = self.get_mean_false_positives()
        calculated_statistics[TN] = self.get_mean_true_negatives()
        calculated_statistics[TP] = self.get_mean_true_positives()
        calculated_statistics[f"{ACC}_plot"] = self.create_model_accuracy_training_plot()
        calculated_statistics[f"{LOSS}_plot"] = self.create_model_loss_training_plot()
        calculated_statistics["percentiles_hist"] = self.create_model_accuracy_percentile_histogram()

        self.plotter.save_plotted_data_to_csv()

        return calculated_statistics

    def create_model_accuracy_training_plot(self):
        return self.__create_model_training_plot(ACC)

    def create_model_loss_training_plot(self):
        return self.__create_model_training_plot(LOSS)

    def __create_model_training_plot(self, metric):
        results_matrix = [record.history[metric] for record in self.__results]
        val_results_matrix = [record.history[f'val_{metric}'] for record in self.__results]

        mean_epoch_values = np.mean(results_matrix, axis=0)
        mean_val_epoch_values = np.mean(val_results_matrix, axis=0)

        return self.plotter.create_plot(metric, mean_epoch_values, mean_val_epoch_values)

    def create_model_accuracy_percentile_histogram(self):
        acc_results = [record.history[ACC][-1] for record in self.__results]
        acc_results = np.round(acc_results, StatisticsUtils.ROUND_DIGITS) * 100
        acc_results.sort()
        return self.plotter.create_histogram(acc_results)

    def get_mean_accuracy(self):
        return self.__calculate_mean_for_metric(ACC) * 100  # %

    def get_mean_loss(self):
        return self.__calculate_mean_for_metric(LOSS) * 100  # %

    def __calculate_mean_for_metric(self, metric):
        final_values = [record.history[metric][-1] for record in self.__results]
        final_values_mean = np.mean(final_values).round(StatisticsUtils.ROUND_DIGITS)
        return final_values_mean

    def get_mean_false_negatives(self):
        return self.__calculate_mean_from_confusion_matrix(FN).astype(int)

    def get_mean_false_positives(self):
        return self.__calculate_mean_from_confusion_matrix(FP).astype(int)

    def get_mean_true_negatives(self):
        return self.__calculate_mean_from_confusion_matrix(TN).astype(int)

    def get_mean_true_positives(self):
        return self.__calculate_mean_from_confusion_matrix(TP).astype(int)

    def __calculate_mean_from_confusion_matrix(self, metric):
        values = [record.history[metric] for record in self.__results]
        return np.mean(values)

    def get_mean_false_rejection_rate(self):
        return self.__calculate_mean_rate_from_confusion_matrix(FN, TP) * 100  # %

    def get_mean_false_acceptance_rate(self):
        return self.__calculate_mean_rate_from_confusion_matrix(FP, TN) * 100  # %

    def __calculate_mean_rate_from_confusion_matrix(self, metric_1, metric_2):
        confusion_matrix = {}
        single_rate_list = []
        for record in self.__results:
            for metric in [FN, FP, TN, TP]:
                confusion_matrix[metric] = record.history[metric]
            single_rate = confusion_matrix[metric_1] / (confusion_matrix[metric_1] + confusion_matrix[metric_2])
            single_rate_list.append(single_rate)
        return np.mean(single_rate_list).round(StatisticsUtils.ROUND_DIGITS)
