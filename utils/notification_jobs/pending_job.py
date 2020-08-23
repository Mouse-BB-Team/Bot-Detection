from utils.slack_notifier import *
from datetime import datetime
from sys import argv


class PendingJobNotification:
    @staticmethod
    def notify():
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
<<<<<<< HEAD
        notifier = SlackNotifier()
        simple_msg = SimpleMessage.new_builder() \
            .with_reporter(argv[1]) \
            .with_commit_hash(f"#{argv[2]}") \
            .with_job_time(start_time) \
            .with_header("PENDING JOB") \
=======
        reporter = argv[1]
        commit_hash = argv[2]
        notifier = SlackNotifier()
        simple_msg = SimpleMessage.new_builder() \
            .with_reporter(reporter) \
            .with_commit_hash(f"#{commit_hash}") \
            .with_job_time(start_time) \
            .with_header("PENDING JOB") \
            .with_summary(f"Pending job for {reporter}: #{commit_hash}") \
>>>>>>> stat_calc_module
            .build()
        notifier.notify(simple_msg)


if __name__ == '__main__':
    PendingJobNotification.notify()
