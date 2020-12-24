import argparse
from datetime import datetime
import subprocess
from os import environ
import tensorflow as tf
from enum import Enum
from ml_models.inceptionV3 import InceptionV3
from utils.slack_notifier.slack_notifier import SlackNotifier
from utils.slack_notifier.message.simple_slack_message import SimpleMessage
from utils.slack_notifier.message.result_slack_message import ResultMessage
from utils.statistics.statistics_utils import StatisticsUtils
from utils.slack_notifier.message.color import Color
from utils.statistics.statistic_metrics.statistic_metrics import Metric
from utils.deserializer.protobuf_deserializer import ProtoLoader
from utils.preproccessing.preprocessor import Preprocessor
from utils.result_terminator.result_terminator import ResultTerminator


DEFAULT_PATH = '/net/archive/groups/plggpchdyplo/dataset2/output'
TRAIN_DIR = '/train'
VAL_DIR = '/val'


class DatasetType(Enum):
    IMAGES = 0
    BINARY = 1


class Job:

    def __init__(self, dataset_path, dataset_type):
        self.is_notify = environ.get("NOTIFY")
        self.commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        self.commit_msg = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()
        self.reporter = subprocess.check_output(['whoami']).decode().strip()
        self.start_time = datetime.now()
        self.notifier = SlackNotifier()

        if dataset_type == DatasetType.BINARY.value:
            proto_loader = ProtoLoader(dataset_path)
            user_dataset = proto_loader.get_list_of_sequences()
            preprocessor = Preprocessor(user_dataset)
            training, validation = preprocessor.get_datasets()
            self.training = tf.data.Dataset.from_tensor_slices(training).batch(128)
            self.validation = tf.data.Dataset.from_tensor_slices(validation).batch(128)
        elif dataset_type == DatasetType.IMAGES.value:
            self.training, self.validation = self.load_datasets(dataset_path)

        self.statistics = None

    @staticmethod
    def load_datasets(dataset_path):
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_path + TRAIN_DIR,
            seed=123,
            image_size=(299, 299),
            batch_size=128)

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_path + VAL_DIR,
            seed=123,
            image_size=(299, 299),
            batch_size=128)

        return train_ds, val_ds

    def __notify_start_job(self):
        if self.is_notify is not None:
            slack_simple = SimpleMessage()
            slack_simple_msg = slack_simple.new_builder() \
                .with_color(Color.BLUE) \
                .with_reporter(f"{self.reporter}") \
                .with_commit_hash(f"#{self.commit_hash}") \
                .with_job_time(self.start_time) \
                .with_header("RUNNING JOB") \
                .with_info_message(f"{self.commit_msg}") \
                .with_summary(f"Running job: {self.commit_msg}") \
                .build()
            self.notifier.notify(slack_simple_msg)

    def __notify_done_job(self, job_time, acc, loss):
        if self.is_notify is not None:
            slack_results = ResultMessage()
            slack_result_msg = slack_results.new_builder() \
                .with_color(Color.GREEN) \
                .with_job_time(f"{job_time}") \
                .with_commit_hash(f"#{self.commit_hash}") \
                .with_reporter(f"{self.reporter}") \
                .with_accuracy(f"{acc}%") \
                .with_loss(f"{loss}%") \
                .with_accuracy_chart(f"{self.statistics.create_model_accuracy_training_plot()}") \
                .with_loss_chart(f"{self.statistics.create_model_loss_training_plot()}") \
                .with_percentile_chart(f"{self.statistics.create_model_accuracy_percentile_histogram()}") \
                .with_summary(f"Completed job #{self.commit_hash}") \
                .with_false_acceptance_rate(f"{self.statistics.get_mean_false_acceptance_rate()}%") \
                .with_false_negatives(f"{self.statistics.get_mean_false_negatives()}") \
                .with_false_positives(f"{self.statistics.get_mean_false_positives()}") \
                .with_false_rejection_rate(f"{self.statistics.get_mean_false_rejection_rate()}%") \
                .with_true_negatives(f"{self.statistics.get_mean_true_negatives()}") \
                .with_true_positives(f"{self.statistics.get_mean_true_positives()}") \
                .build()

            self.notifier.notify(slack_result_msg)

    def __notify_crash_job(self, exception):
        if self.is_notify is not None:
            crashed_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            slack_simple = SimpleMessage()
            slack_err_msg = slack_simple.new_builder() \
                .with_color(Color.RED) \
                .with_reporter(f"{self.reporter}") \
                .with_commit_hash(f"#{self.commit_hash}") \
                .with_job_time(crashed_time) \
                .with_header("CRASHED JOB") \
                .with_info_message(f"Job crashed: {exception}") \
                .build()
            self.notifier.notify(slack_err_msg)
        else:
            raise exception

    def __compute_statistics(self, result):
        self.statistics = StatisticsUtils(result)
        acc = self.statistics.get_mean_accuracy()
        loss = self.statistics.get_mean_loss()
        return acc, loss

    def __terminate(self, acc, loss):
        results_dict = {"commit_hash": self.commit_hash,
                        Metric.ACC.value: acc,
                        Metric.LOSS.value: loss}

        ResultTerminator(["commit_hash", Metric.ACC.value, Metric.LOSS.value]).terminate(results_dict)

    def run(self, model_execution_count):
        self.__notify_start_job()
        try:
            result = []

            mirrored_strategy = tf.distribute.MirroredStrategy()

            for i in range(model_execution_count):
                with mirrored_strategy.scope():
                    model = InceptionV3(self.training, self.validation)
                    result.append(model.run())

            job_time = self.__compute_job_time()
            acc, loss = self.__compute_statistics(result)
            self.__notify_done_job(job_time, acc, loss)
            self.__terminate(acc, loss)

        except Exception as e:
            self.__notify_crash_job(e)

    def __compute_job_time(self):
        return datetime.now() - self.start_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run ML model')
    parser.add_argument('-d', required=False, type=str, help=f'directory to dataset (default {DEFAULT_PATH})', default=DEFAULT_PATH)
    parser.add_argument('-t', required=False, type=int, help='model execution count (default 1)', default=1)
    parser.add_argument('--type', required=False, type=int, help='0 for images, 1 for binary dataset (default 0)', default=0)
    args = parser.parse_args()
    directory = args.d
    count = args.t
    dataset_type = args.type

    job = Job(directory, dataset_type)
    job.run(count)
