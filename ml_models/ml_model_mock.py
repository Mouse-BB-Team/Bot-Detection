from random import uniform, randrange
import time


class MlModelMock:
    def run(self):
        # time.sleep(randrange(2, 10))
        result_mock = {"metrics": {
            "accuracy": [uniform(0.8, 1.0) for _ in range(3)],
            "val_accuracy": [uniform(0.5, 1.0) for _ in range(3)],
            "loss": [uniform(0.45, 0.6) for _ in range(3)],
            "val_loss": [uniform(0.45, 0.6) for _ in range(3)],
            "true_positives": randrange(8300, 8800),
            "false_negatives": randrange(600, 850),
            "false_positives": randrange(200, 600),
            "true_negatives": randrange(8000, 9500),
            "far": [uniform(0.04, 0.06) for _ in range(2)],
            "val_far": [uniform(0.04, 0.06) for _ in range(2)],
            "frr": [uniform(0.05, 0.2) for _ in range(2)],
            "val_frr": [uniform(0.05, 0.2) for _ in range(2)]
        }}
        return result_mock
