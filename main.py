from ml_models.light_ml_model import LightMlModel
from utils.task_executor.task_executor import TaskExecutor
from utils.slack_notifier.slack_notifier import SlackNotifier
from utils.slack_notifier.simple_slack_message import SimpleMessage
from utils.slack_notifier.result_slack_message import ResultMessage
from utils.statistics.statistics_utils import StatisticsUtils
from utils.slack_notifier.message_color import Color
from datetime import datetime
import subprocess

if __name__ == '__main__':
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        start_time = datetime.now()
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

        slack_simple = SimpleMessage()
        slack_simple_msg = slack_simple.new_builder() \
            .with_color(Color.BLUE) \
            .with_reporter("plgkamilkalis") \
            .with_commit_hash(commit_hash) \
            .with_job_time(start_time) \
            .with_header("TEST JOB") \
            .with_info_message("Starting test job from prometheus") \
            .build()

        notifier = SlackNotifier()
        notifier.notify(slack_simple_msg)

        model = LightMlModel()
        executor = TaskExecutor(model)
        result = executor.start_execution(2)

        end_time = datetime.now()
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        job_time = end_time - start_time

        statistics = StatisticsUtils(result)
        stat_results = statistics.calculate_all_statistics()

        slack_results = ResultMessage()
        slack_result_msg = slack_results.new_builder() \
            .with_color(Color.GREEN) \
            .with_job_time(job_time) \
            .with_commit_hash(commit_hash) \
            .with_reporter("plgkamilkalis") \
            .with_accuracy(stat_results['accuracy']) \
            .with_accuracy_chart(stat_results['accuracy_plot']) \
            .with_false_acceptance_rate(stat_results['false_acceptance_rate']) \
            .with_false_negatives(statistics.get_mean_false_negatives()) \
            .with_false_positives(statistics.get_mean_false_positives()) \
            .with_false_rejection_rate(statistics.get_mean_false_rejection_rate()) \
            .with_loss(stat_results['loss']) \
            .with_loss_chart(stat_results["loss_plot"]) \
            .with_percentile_chart(stat_results['percentiles_hist']) \
            .with_true_negatives(statistics.get_mean_true_negatives()) \
            .with_true_positives(statistics.get_mean_true_positives()) \
            .with_summary("Completed job") \
            .build()

        notifier.notify(slack_result_msg)
    except Exception as e:
        slack_err_msg = slack_simple.new_builder() \
            .with_color(Color.RED) \
            .with_reporter("plgkamilkalis") \
            .with_commit_hash(commit_hash) \
            .with_job_time(start_time) \
            .with_header("CRASHED JOB") \
            .with_info_message("Job crashed. Check logs!") \
            .build()
        notifier.notify(slack_err_msg)
        print(e)

