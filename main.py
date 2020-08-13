from ml_models.piotr_model import PiotrModel
from ml_models.light_ml_model import LightMlModel
from utils.task_executor.task_executor import TaskExecutor
from utils.slack_notifier.slack_notifier import SlackNotifier
from utils.slack_notifier.message.simple_slack_message import SimpleMessage
from utils.slack_notifier.message.result_slack_message import ResultMessage
from utils.statistics.statistics_utils import StatisticsUtils
from utils.slack_notifier.message.color import Color
from datetime import datetime
import subprocess
from os import environ

NOTIFY = environ.get("NOTIFY")

if __name__ == '__main__':
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
    start_time = datetime.now()

    if NOTIFY is not None:
        slack_simple = SimpleMessage()
        slack_simple_msg = slack_simple.new_builder() \
            .with_color(Color.BLUE) \
            .with_reporter("plgkamilkalis") \
            .with_commit_hash(f"#{commit_hash}") \
            .with_job_time(start_time) \
            .with_header("RUNNING JOB") \
            .with_info_message("Starting test job from prometheus") \
            .build()
        notifier = SlackNotifier()
        notifier.notify(slack_simple_msg)

    try:
        model = PiotrModel()
        # executor = TaskExecutor(model)
        # result = executor.start_execution(2)
        result = [model.run()]

        end_time = datetime.now()
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')

        job_time = end_time - start_time

        statistics = StatisticsUtils(result)
        # stat_results = statistics.calculate_all_statistics()

        if NOTIFY is not None:
            slack_results = ResultMessage()
            slack_result_msg = slack_results.new_builder() \
                .with_color(Color.GREEN) \
                .with_job_time(f"{job_time}") \
                .with_commit_hash(f"#{commit_hash}") \
                .with_reporter("plgkamilkalis") \
                .with_accuracy(f"{statistics.get_mean_accuracy()}%") \
                .with_accuracy_chart(f"{statistics.create_model_accuracy_training_plot()}") \
                .with_loss_chart("https://img.pakamera.net/i1/7/379/obrazy-i-plakaty-12320957_6788571379.jpg") \
                .with_percentile_chart("https://img.pakamera.net/i1/7/379/obrazy-i-plakaty-12320957_6788571379.jpg") \
                .with_false_acceptance_rate("stat_results['false_acceptance_rate']") \
                .with_false_negatives("statistics.get_mean_false_negatives()") \
                .with_false_positives("statistics.get_mean_false_positives()") \
                .with_false_rejection_rate("statistics.get_mean_false_rejection_rate()") \
                .with_loss("stat_results['loss']") \
                .with_true_negatives("statistics.get_mean_true_negatives()") \
                .with_true_positives("statistics.get_mean_true_positives()") \
                .with_summary("Completed job") \
                .build()

            notifier.notify(slack_result_msg)

    except Exception as e:
        if NOTIFY is not None:
            crashed_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            slack_err_msg = slack_simple.new_builder() \
                .with_color(Color.RED) \
                .with_reporter("plgkamilkalis") \
                .with_commit_hash(f"#{commit_hash}") \
                .with_job_time(crashed_time) \
                .with_header("CRASHED JOB") \
                .with_info_message("Job crashed. Check logs!") \
                .build()
            notifier.notify(slack_err_msg)
            print(e)
