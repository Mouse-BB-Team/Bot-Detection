from typing import AnyStr, Dict
from utils.slack_notifier.message.color import Color


class SimpleMessage:

    @staticmethod
    def new_builder():
        return SimpleMessage.__MessageBuilder()

    class __MessageBuilder:

        def __init__(self):
            self.__summary = ''
            self.__header = ''
            self.__color = Color.WHITE
            self.__reporter = ''
            self.__job_time = ''
            self.__commit_hash = ''
            self.__info_message = None

        def with_summary(self, summary: AnyStr):
            self.__summary = summary
            return self

        def with_header(self, header: AnyStr):
            self.__header = header
            return self

        def with_color(self, color):
            self.__color = color
            return self

        def with_reporter(self, reporter: AnyStr):
            self.__reporter = reporter
            return self

        def with_job_time(self, job_time: AnyStr):
            self.__job_time = job_time
            return self

        def with_commit_hash(self, commit_hash: AnyStr):
            self.__commit_hash = commit_hash
            return self

        def with_info_message(self, info_message: AnyStr):
            self.__info_message = info_message
            return self

        @staticmethod
        def __create_fields(fields: Dict[AnyStr, AnyStr]):
            return [{"title": key, "value": value} for key, value in fields.items()]

        def build(self):
            header = {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": self.__header,
                    "emoji": True
                }
            }

            job_info = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Reporter*: %s \t *Commit*: %s \t *Job time*: %s" % (
                    self.__reporter, self.__commit_hash, self.__job_time)
                }
            }

            blocks = [header, job_info]

            if self.__info_message is not None:
                info_block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self.__info_message
                    }
                }

                blocks.append(info_block)

            message = {
                "attachments": [
                    {
                        "color": self.__color.value,
                        "fallback": self.__summary,
                        "blocks": blocks
                    }
                ]
            }

            return message
