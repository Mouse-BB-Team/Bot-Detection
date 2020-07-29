from typing import AnyStr, Dict
from enum import Enum


class Message:

    class Color(Enum):
        GREEN = "#36a64f"
        RED = "#ff004d"
        BLUE = "#2092e7"

    @staticmethod
    def new_builder():
        return Message.__MessageBuilder()

    class __MessageBuilder:

        def __init__(self):
            self.__summary = ''
            self.__header = ''
            self.__author = ''
            self.__subheader = ''
            self.__text = ''
            self.__fields = {}
            self.__color = Message.Color.BLUE
            self.__notifier_name = ''
            self.__notifier_icon = ''
            self.__timestamp = ''

        def with_summary(self, summary: AnyStr):
            self.__summary = summary
            return self

        def with_header(self, header: AnyStr):
            self.__header = header
            return self

        def with_author(self, author: AnyStr):
            self.__author = author
            return self

        def with_subheader(self, subheader: AnyStr):
            self.__subheader = subheader
            return self

        def with_text(self, text: AnyStr):
            self.__text = text
            return self

        def with_fields(self, fields: Dict[AnyStr, AnyStr]):
            self.__fields = fields
            return self

        def with_color(self, color):
            self.__color = color
            return self

        def with_notifier_name(self, notifier_name: AnyStr):
            self.__notifier_name = notifier_name
            return self

        def with_notifier_icon(self, notifier_icon: AnyStr):
            self.__notifier_icon = notifier_icon
            return self

        def with_timestamp(self, timestamp: AnyStr):
            self.__timestamp = timestamp
            return self

        @staticmethod
        def __create_fields(fields: Dict[AnyStr, AnyStr]):
            result = list()
            for key in fields.keys():
                result.append({"title": key, "value": fields[key]})
            return result

        def build(self):
            message = {
                "attachments": [
                    {
                        "fallback": self.__summary,
                        "color": self.__color.value,
                        "pretext": self.__header,
                        "author_name": self.__author,
                        "title": self.__subheader,
                        "text": self.__text,
                        "fields": self.__create_fields(self.__fields),
                        "footer": self.__notifier_name,
                        "footer_icon": self.__notifier_icon,
                        "ts": self.__timestamp
                    }
                ]
            }

            return message
