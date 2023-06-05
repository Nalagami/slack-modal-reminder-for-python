import time
from datetime import datetime


class Modal:
    """
    modal class
    """

    def __init__(
        self,
        destination="to-me",
        number_of_times="onece-remind",
        frequency="every-day",
    ):
        """
        初期化
        :param destination:宛先
        :param number_of_times:リマインド回数
        :param frequency:リマインド周期
        """
        self.__destination = destination
        self.__number_of_times = number_of_times
        self.__frequency = frequency
        self.__modal = self.make_modal()

    def update_modal(self):
        self.__modal = self.make_modal()
        return self.get_modal()

    def get_modal(self):
        """
        modalを取得
        """
        return self.__modal

    def set_destination(self, value):
        self.__destination = value

    def set_number_of_times(self, value):
        self.__number_of_times = value

    def set_frequencyy(self, value):
        self.__frequency = value

    # リマインド内容入力ブロックを作成
    def make_remind_message_block(self):
        return {
            "type": "input",
            "block_id": "content-block",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action",
            },
            # これはモーダル上での見た目を調整するものです
            # 同様に "placeholder" を指定することも可能です
            "label": {
                "type": "plain_text",
                "text": "リマインド内容",
            },
        }

    # リマインド送信先カテゴリ選択ブロックを作成
    def make_destination_block(self):
        return {
            "type": "section",
            "block_id": "destination-block",
            "text": {
                "type": "mrkdwn",
                "text": "*宛先*",
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                },
                "initial_option": {
                    "text": {"type": "plain_text", "text": "自分自身"},
                    "value": "to-me",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "自分自身"},
                        "value": "to-me",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "チャンネル",
                        },
                        "value": "to-channel",
                    },
                ],
                "action_id": "destination-action",
            },
        }

    # リマインド送信先カテゴリブロックを作成
    def make_channel_block(self):
        return {
            "type": "section",
            "block_id": "channel-block",
            "text": {
                "type": "mrkdwn",
                "text": "*送信先チャンネル*",
            },
            "accessory": {
                "type": "channels_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "リマインダーを設定したいチャンネルを選んでください",
                },
                "action_id": "channel-action",
            },
        }

    # リマインド頻度選択ブロックを作成
    def make_number_of_times_block(self):
        return {
            "type": "section",
            "block_id": "number-of-times-block",
            "text": {
                "type": "mrkdwn",
                "text": "*リマインド周期*",
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                },
                "initial_option": {
                    "text": {"type": "plain_text", "text": "1回のみ"},
                    "value": "onece-remind",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "1回のみ"},
                        "value": "onece-remind",
                    },
                    {
                        "text": {"type": "plain_text", "text": "繰り返し"},
                        "value": "periodic-remind",
                    },
                ],
                "action_id": "number-of-times-action",
            },
        }

    # リマインド間隔入力ブロックを作成
    def make_frequency_block(self):
        return {
            "type": "section",
            "block_id": "frequency-block",
            "text": {
                "type": "mrkdwn",
                "text": "*間隔*",
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                },
                "initial_option": {
                    "text": {"type": "plain_text", "text": "毎日"},
                    "value": "every-day",
                },
                "options": [
                    {
                        "text": {"type": "plain_text", "text": "毎日"},
                        "value": "every-day",
                    },
                    {
                        "text": {"type": "plain_text", "text": "毎週"},
                        "value": "every-week",
                    },
                    {
                        "text": {"type": "plain_text", "text": "毎月"},
                        "value": "every-month",
                    },
                    {
                        "text": {"type": "plain_text", "text": "毎年"},
                        "value": "every-year",
                    },
                ],
                "action_id": "frequency-action",
            },
        }

    # 日付・時間ブロックを作成
    def make_datetime_block(self):
        return {
            "type": "input",
            "block_id": "datetime-block",
            "element": {
                "type": "datetimepicker",
                "initial_date_time": int(time.time()),
                "action_id": "datetime-action",
            },
            "label": {
                "type": "plain_text",
                "text": "日時",
            },
        }

    # 日付入力ブロックを作成
    def make_day_block(self):
        return {
            "type": "input",
            "block_id": "day-block",
            "element": {
                "type": "number_input",
                "is_decimal_allowed": False,
                "min_value": "1",
                "max_value": "31",
                "action_id": "day-action",
            },
            "label": {
                "type": "plain_text",
                "text": "日付",
            },
        }

    # 曜日ブロックを作成
    def make_day_of_week_block(self):
        return {
            "type": "input",
            "block_id": "day-of-week-block",
            "element": {
                "type": "checkboxes",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "日曜日",
                        },
                        "value": "sun",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "月曜日",
                        },
                        "value": "mon",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "火曜日",
                        },
                        "value": "tue",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "水曜日",
                        },
                        "value": "wed",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "木曜日",
                        },
                        "value": "thu",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "金曜日",
                        },
                        "value": "fri",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "土曜日",
                        },
                        "value": "sat",
                    },
                ],
                "action_id": "day-of-week-action",
            },
            "label": {
                "type": "plain_text",
                "text": "曜日",
            },
        }

    # 時間ブロックを作成
    def make_time_block(self):
        return {
            "type": "input",
            "block_id": "time-block",
            "element": {
                "type": "timepicker",
                "initial_time": datetime.now().strftime("%H:%M"),
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select time",
                },
                "action_id": "time-action",
            },
            "label": {
                "type": "plain_text",
                "text": "時間",
            },
        }

    def make_modal(self):
        """
        modalを生成する関数
        """
        blocks = []
        blocks.append(self.make_remind_message_block())
        blocks.append(self.make_destination_block())

        if self.__destination == "to-channel":
            blocks.append(self.make_channel_block())

        blocks.append(self.make_number_of_times_block())

        if self.__number_of_times == "periodic-remind":
            blocks.append(self.make_frequency_block())
            if self.__frequency == "every-year":
                blocks.append(self.make_datetime_block())
            elif self.__frequency == "every-month":
                blocks.append(self.make_day_block())
                blocks.append(self.make_time_block())
            elif self.__frequency == "every-week":
                blocks.append(self.make_day_of_week_block())
                blocks.append(self.make_time_block())
            elif self.__frequency == "every-day":
                blocks.append(self.make_time_block())
        elif self.__number_of_times == "onece-remind":
            blocks.append(self.make_datetime_block())

        return {
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "リマインダーセット"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": blocks,
        }
