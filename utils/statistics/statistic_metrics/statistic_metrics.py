from enum import Enum


class Metric(Enum):
    ACC = 'accuracy'
    LOSS = 'loss'
    FP = 'false_positives'
    FN = 'false_negatives'
    TN = 'true_negatives'
    TP = 'true_positives'
    FAR = 'false_acceptance_rate'
    FRR = 'false_rejection_rate'
    ACC_PLOT = 'accuracy_plot'
    LOSS_PLOT = 'loss_plot'
    PERCENTILES_HISTOGRAM = 'percentiles_hist'
