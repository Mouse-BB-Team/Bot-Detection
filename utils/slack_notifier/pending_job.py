from slack_notifier import SlackNotifier
from simple_slack_message import SimpleMessage
from datetime import datetime
from sys import argv

if __name__ == '__main__':
    start_time = datetime.now()
    notifier = SlackNotifier()
    simple_msg = SimpleMessage.new_builder() \
        .with_reporter(argv[1]) \
        .with_commit_hash(f"#{argv[2]}") \
        .with_job_time(start_time) \
        .with_header("Pending job") \
        .with_info_message("Starting test job from prometheus") \
        .build()
    notifier.notify(simple_msg)
