from typing import AnyStr
from utils.slack_notifier.message.color import Color


class ResultMessage:

    @staticmethod
    def new_builder():
        return ResultMessage.__MessageBuilder()

    class __MessageBuilder:

        def __init__(self):
            self.__summary = ''
            self.__color = Color.WHITE
            self.__reporter = ''
            self.__job_time = ''
            self.__accuracy = ''
            self.__loss = ''
            self.__false_negatives = ''
            self.__false_positives = ''
            self.__true_negatives = ''
            self.__true_positives = ''
            self.__accuracy_chart = ''
            self.__loss_chart = ''
            self.__percentile_chart = ''
            self.__false_rejection_rate = ''
            self.__false_acceptance_rate = ''
            self.__commit_hash = ''

        def with_summary(self, summary: AnyStr):
            self.__summary = summary
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

        def with_accuracy(self, accuracy: AnyStr):
            self.__accuracy = accuracy
            return self

        def with_loss(self, loss: AnyStr):
            self.__loss = loss
            return self

        def with_false_negatives(self, false_negatives: AnyStr):
            self.__false_negatives = false_negatives
            return self

        def with_false_positives(self, false_positives: AnyStr):
            self.__false_positives = false_positives
            return self

        def with_true_negatives(self, true_negatives: AnyStr):
            self.__true_negatives = true_negatives
            return self

        def with_true_positives(self, true_positives: AnyStr):
            self.__true_positives = true_positives
            return self

        def with_accuracy_chart(self, accuracy_chart: AnyStr):
            self.__accuracy_chart = accuracy_chart
            return self

        def with_loss_chart(self, loss_chart: AnyStr):
            self.__loss_chart = loss_chart
            return self

        def with_percentile_chart(self, percentile_chart: AnyStr):
            self.__percentile_chart = percentile_chart
            return self

        def with_false_rejection_rate(self, false_rejection_rate: AnyStr):
            self.__false_rejection_rate = false_rejection_rate
            return self

        def with_false_acceptance_rate(self, false_acceptance_rate: AnyStr):
            self.__false_acceptance_rate = false_acceptance_rate
            return self

        def with_commit_hash(self, commit_hash: AnyStr):
            self.__commit_hash = commit_hash
            return self

        def build(self):
            message = {
                "attachments": [
                    {
                        "color": self.__color.value,
                        "fallback": self.__summary,
                        "blocks": [
                            {
                                "type": "header",
                                "text": {
                                    "type": "plain_text",
                                    "text": "FINISHED JOB",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "*Reporter*: %s \t *Commit*: %s \t *Job time*: %s" % (self.__reporter, self.__commit_hash, self.__job_time)
                                }
                            },
                            {
                                "type": "header",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Results:",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "plain_text",
                                        "text": "Accuracy: %s" % self.__accuracy,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "False negatives: %s" % self.__false_negatives,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "Loss: %s" % self.__loss,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "False positives: %s" % self.__false_positives,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "False rejection rate: %s" % self.__false_rejection_rate,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "True negatives: %s" % self.__true_negatives,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "False acceptance rate: %s" % self.__false_acceptance_rate,
                                        "emoji": True
                                    },
                                    {
                                        "type": "plain_text",
                                        "text": "True positives: %s" % self.__true_positives,
                                        "emoji": True
                                    }
                                ]
                            },
                            {
                                "type": "header",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Charts:",
                                    "emoji": True
                                }
                            },
                            {
                                "type": "image",
                                "title": {
                                    "type": "plain_text",
                                    "text": "Accuracy history",
                                    "emoji": True
                                },
                                "image_url": self.__accuracy_chart,
                                "alt_text": "Accuracy history"
                            },
                            {
                                "type": "image",
                                "title": {
                                    "type": "plain_text",
                                    "text": "Loss history",
                                    "emoji": True
                                },
                                "image_url": self.__loss_chart,
                                "alt_text": "Loss history"
                            },
                            {
                                "type": "image",
                                "title": {
                                    "type": "plain_text",
                                    "text": "Percentile",
                                    "emoji": True
                                },
                                "image_url": self.__percentile_chart,
                                "alt_text": "Percentile"
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "<%s|Accuracy chart - URL>" % self.__accuracy_chart
                                }
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "<%s|Loss chart - URL>" % self.__loss_chart
                                }
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "<%s|Percentile chart - URL>" % self.__percentile_chart
                                }
                            }
                        ]
                    }
                ]
            }

            return message
