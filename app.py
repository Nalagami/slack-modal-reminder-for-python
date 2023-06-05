# serverless-python-requirements を使って zip 圧縮しておいた依存ライブラリの読み込み
try:
    import unzip_requirements
except ImportError:
    pass

import os
import logging
from datetime import datetime
from slack_bolt import App, Ack, BoltContext
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from lib.modal_model import Modal
from lib.remind_model import Remind

# ロギングをwarningレベルに設定
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.WARNING)

app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET", ""),
    token=os.environ.get("SLACK_BOT_TOKEN", ""),
    # lambda用パラメータ
    process_before_response=True,
)


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


# modalを表示する関数
@app.shortcut("send-reminder-modal")
def send_reminder_modal(ack: Ack, body: dict, client: WebClient):
    ack()

    modal = Modal()
    client.views_open(
        trigger_id=body["trigger_id"],
        view=modal.get_modal(),
    )


# 宛先を変更したとき、modalを更新する関数
@app.action("destination-action")
def update_destination_modal(
    ack: Ack, payload: dict, body: dict, client: WebClient
):
    values = body["view"]["state"]["values"]
    destination = (
        values.get("destination-block", {})
        .get("destination-action", {})
        .get("selected_option", {})
        .get("value", "")
    )
    number_of_times = (
        values.get("number-of-times-block", {})
        .get("number-of-times-action", {})
        .get("selected_option", {})
        .get("value", "")
    )
    frequency = (
        values.get("frequency-block", {})
        .get("frequency-action", {})
        .get("selected_option", {})
        .get("value", "")
    )

    modal = Modal(destination, number_of_times, frequency)

    client.views_update(
        view_id=body.get("view").get("id"),
        hash=body.get("view").get("hash"),
        # 入力された送信先カテゴリに応じて出し分け
        view=modal.make_modal(),
    )

    ack()


# 送信先チャンネル設定時の処理
# 何も処理しない
@app.action("channel-action")
def destination_input_action(
    ack: Ack, payload: dict, body: dict, client: WebClient
):
    ack()


# リマインド周期選択時
@app.action("number-of-times-action")
def change_datetime_action(
    ack: Ack, payload: dict, body: dict, client: WebClient
):
    values = body["view"]["state"]["values"]
    destination = (
        values.get("destination-block", {})
        .get("destination-action", {})
        .get("selected_option", {})
        .get("value", "")
    )
    number_of_times = (
        values.get("number-of-times-block", {})
        .get("number-of-times-action", {})
        .get("selected_option", {})
        .get("value", "")
    )
    frequency = (
        (
            values.get("frequency-block", {})
            .get("frequency-action", {})
            .get("selected_option", {})
            .get("value", "")
        )
        if number_of_times == "onece-remind"
        else "every-day"
    )

    modal = Modal(destination, number_of_times, frequency)

    client.views_update(
        view_id=body.get("view").get("id"),
        hash=body.get("view").get("hash"),
        # 入力されたリマインド周期に応じて出し分け
        view=modal.make_modal(),
    )

    ack()


# リマインド周期選択時
@app.action("frequency-action")
def periodic_datetime_action(
    ack: Ack, payload: dict, body: dict, client: WebClient
):
    values = body["view"]["state"]["values"]
    destination = (
        values.get("destination-block", {})
        .get("destination-action", {})
        .get("selected_option", {})
        .get("value", "")
    )
    number_of_times = (
        values.get("number-of-times-block", {})
        .get("number-of-times-action", {})
        .get("selected_option", {})
        .get("value", "")
    )
    frequency = (
        values.get("frequency-block", {})
        .get("frequency-action", {})
        .get("selected_option", {})
        .get("value", "")
    )

    modal = Modal(destination, number_of_times, frequency)

    client.views_update(
        view_id=body.get("view").get("id"),
        hash=body.get("view").get("hash"),
        # 入力されたリマインド周期に応じて出し分け
        view=modal.make_modal(),
    )

    ack()


@app.view("modal-id")
def handle_view_events(
    ack: Ack,
    view: dict,
    client: WebClient,
    context: BoltContext,
    logger: logging.Logger,
):
    inputs = view["state"]["values"]

    remind = Remind(inputs=inputs, client=client)

    # DMでリマインドコマンドを送信
    client.chat_postMessage(
        channel=context.user_id,
        text="以下のメッセージを送信してください！",
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "以下のメッセージを送信してください！"},
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"> {remind.make_remind_message()}",
                },
            },
        ],
    )

    # 正常パターン
    logger.info(f"Make remind success!")

    ack()


# アプリを起動
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


# lambdaのときのみ実行
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# ロギングを AWS Lambda 向けに初期化
SlackRequestHandler.clear_all_log_handlers()
# logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.WARNING)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
