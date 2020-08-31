import multiprocessing
import re

from ml_models.piotr_model import PiotrModel
from ml_models.light_ml_model import LightMlModel
from ml_models.ml_model import MlModelExample
from ml_models.convolutional_network import ConvolutionalNetwork
from utils.task_executor.task_executor import TaskExecutor
from utils.slack_notifier.slack_notifier import SlackNotifier
from utils.slack_notifier.message.simple_slack_message import SimpleMessage
from utils.slack_notifier.message.result_slack_message import ResultMessage
from utils.statistics.statistics_utils import StatisticsUtils
from utils.slack_notifier.message.color import Color
from datetime import datetime
from utils.result_terminator.result_terminator import ResultTerminator
import subprocess
from os import environ
from utils.statistics.statistic_metrics.statistic_metrics import Metric

NOTIFY = environ.get("NOTIFY")

if __name__ == '__main__':
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
    commit_msg = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()
    reporter = subprocess.check_output(['whoami']).decode().strip()
    start_time = datetime.now()

    if NOTIFY is not None:
        slack_simple = SimpleMessage()
        slack_simple_msg = slack_simple.new_builder() \
            .with_color(Color.BLUE) \
            .with_reporter(f"{reporter}") \
            .with_commit_hash(f"#{commit_hash}") \
            .with_job_time(start_time) \
            .with_header("RUNNING JOB") \
            .with_info_message(f"{commit_msg}") \
            .with_summary(f"Running job: {commit_msg}") \
            .build()
        notifier = SlackNotifier()
        notifier.notify(slack_simple_msg)

    def obtain_gpus(q):
        import tensorflow as tf
        gpus = tf.config.experimental.list_physical_devices('GPU')
        print(gpus)
        q.put(gpus)

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=obtain_gpus, args=(q,))
    p.start()
    p.join()

    gpus = q.get()

    gpus = [device.name for device in gpus]
    gpus = [re.sub('physical_device', 'device', device) for device in gpus]

    try:
        model = ConvolutionalNetwork()

        executor = TaskExecutor(model, gpus)
        result = executor.start_execution(len(gpus))

        end_time = datetime.now()
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')

        job_time = end_time - start_time

        statistics = StatisticsUtils(result)

        acc = statistics.get_mean_accuracy()
        loss = statistics.get_mean_loss()
        if NOTIFY is not None:
            slack_results = ResultMessage()
            slack_result_msg = slack_results.new_builder() \
                .with_color(Color.GREEN) \
                .with_job_time(f"{job_time}") \
                .with_commit_hash(f"#{commit_hash}") \
                .with_reporter(f"{reporter}") \
                .with_accuracy(f"{acc}%") \
                .with_loss(f"{loss}%") \
                .with_accuracy_chart(f"{statistics.create_model_accuracy_training_plot()}") \
                .with_loss_chart(f"{statistics.create_model_loss_training_plot()}") \
                .with_percentile_chart(f"{statistics.create_model_accuracy_percentile_histogram()}") \
                .with_summary(f"Completed job #{commit_hash}") \
                .build()
                # .with_false_acceptance_rate(f"{statistics.get_mean_false_acceptance_rate()}%") \
                # .with_false_negatives(f"{statistics.get_mean_false_negatives()}") \
                # .with_false_positives(f"{statistics.get_mean_false_positives()}") \
                # .with_false_rejection_rate(f"{statistics.get_mean_false_rejection_rate()}%") \
                # .with_true_negatives(f"{statistics.get_mean_true_negatives()}") \
                # .with_true_positives(f"{statistics.get_mean_true_positives()}") \

            notifier.notify(slack_result_msg)

        results_dict = {"commit_hash": commit_hash,
                        Metric.ACC.value: acc,
                        Metric.LOSS.value: loss}

        ResultTerminator(["commit_hash", Metric.ACC.value, Metric.LOSS.value]).terminate(results_dict)

    except Exception as e:
        if NOTIFY is not None:
            crashed_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            slack_err_msg = slack_simple.new_builder() \
                .with_color(Color.RED) \
                .with_reporter(f"{reporter}") \
                .with_commit_hash(f"#{commit_hash}") \
                .with_job_time(crashed_time) \
                .with_header("CRASHED JOB") \
                .with_info_message(f"Job crashed: {e}") \
                .build()
            notifier.notify(slack_err_msg)
        else:
            raise e
