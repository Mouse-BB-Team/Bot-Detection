from ..slack_notifier.slack_notifier import SlackNotifier
from ..slack_notifier.simple_slack_message import SimpleMessage
from datetime import datetime
from sys import argv


class PendingJobNotification:
    @staticmethod
    def notify():
        start_time = datetime.now()
        notifier = SlackNotifier()
        simple_msg = SimpleMessage.new_builder() \
            .with_reporter(argv[1]) \
            .with_commit_hash(f"#{argv[2]}") \
            .with_job_time(start_time) \
            .with_header("Pending job") \
            .build()
        notifier.notify(simple_msg)


if __name__ == '__main__':
    PendingJobNotification.notify()
