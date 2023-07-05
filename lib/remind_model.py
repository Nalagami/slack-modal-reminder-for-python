from slack_sdk import WebClient
from datetime import datetime


class Remind:
    """
    リマインダーセットのためのオブジェクト
    """

    def __init__(self, inputs={}, client=WebClient()):
        # TODO: clientの宣言順に処理が依存(channel名の取得) を解消
        self.__client = client
        self.__content = (
            inputs.get("content-block", {})
            .get("plain_text_input-action", {})
            .get("value", "")
        )
        self.__destination = (
            inputs.get("destination-block", {})
            .get("destination-action", {})
            .get("selected_option", {})
            .get("value", "")
        )
        self.__number_of_times = (
            inputs.get("number-of-times-block", {})
            .get("number-of-times-action", {})
            .get("selected_option", {})
            .get("value", "")
        )
        self.__channel_id = (
            inputs.get("channel-block", {})
            .get("channel-action", {})
            .get("selected_channel", "")
        )
        self.__frequency = (
            inputs.get("frequency-block", {})
            .get("frequency-action", {})
            .get("selected_option", {})
            .get("value", "")
        )
        self.__unix_datetime = (
            inputs.get("datetime-block", {})
            .get("datetime-action", {})
            .get("selected_date_time", 0)
        )
        # 1~31 の数値
        self.__remind_day = (
            inputs.get("day-block", {}).get("day-action", {}).get("value", "1")
        )
        self.__remind_day_of_week = [
            input.get("value", "")
            for input in inputs.get("day-of-week-block", {})
            .get("day-of-week-action", {})
            .get("selected_options", [])
        ]
        # HH:MM 形式の文字列
        self.__remind_time = (
            inputs.get("time-block", {})
            .get("time-action", {})
            .get("selected_time", "")
        )
        self.__channel_name = (
            self.search_channel_name() if self.__channel_id != "" else ""
        )

    def search_channel_name(self):
        return (
            self.__client.conversations_info(channel=self.__channel_id)
            .get("channel", {})
            .get("name")
        )

    def make_remind_time(self):
        if self.__number_of_times == "onece-remind":
            return f'on {datetime.fromtimestamp(self.__unix_datetime).strftime("%m/%d/%Y")} at {datetime.fromtimestamp(self.__unix_datetime).strftime("%H:%M")}'
        elif self.__number_of_times == "periodic-remind":
            if self.__frequency == "every-day":
                return f"at {self.__remind_time} everyday"
            if self.__frequency == "every-week":
                str_day_of_week = ""
                dict_day_of_week = {
                    "sun": "Sunday",
                    "mon": "Monday",
                    "tue": "Tuesday",
                    "wed": "Wednesday",
                    "thu": "Thursday",
                    "fri": "Friday",
                    "sat": "Saturday",
                }
                for day_of_week in self.__remind_day_of_week:
                    str_day_of_week += dict_day_of_week[day_of_week]
                    str_day_of_week += ","
                return f"at {self.__remind_time} on every {str_day_of_week}"
            if self.__frequency == "every-month":
                return f"at {self.__remind_time} on {self.__remind_day} every month"
            if self.__frequency == "every-year":
                return f'on {datetime.fromtimestamp(self.__unix_datetime).strftime("%m/%d")} at {datetime.fromtimestamp(self.__unix_datetime).strftime("%H:%M")} every year'

    def make_remind_message(self):
        return f'/remind {self.__channel_name} "{self.__content}" {self.make_remind_time()}'

    # TODO: 例外処理を追加(日付が現在時刻より前だった場合)

    def get_my_instance_var_names(self):
        return vars(self)

    def is_addressed_to_myself(self):
        """
        宛先が自分自身かどうか判別する関数

        channel_id があればFalse(自分自身ではない) それ以外はTrue
        """
        return False if self.__channel_id != "" else True
