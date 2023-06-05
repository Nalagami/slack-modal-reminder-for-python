# slack-modal-reminder-for-python

## Overview
slack のリマインダーコマンドを生成するApp

## Requirement
```
aws cli 2.11.25
npm 9.6.2
serverless-framework
- Framework Core: 3.32.2 (local) 3.31.0 (global)
- Plugin: 6.2.3
- SDK: 4.3.2
python 3.9
```

## Usage
- グローバルショートカットから「リマインダーコマンド生成」を選択
- 必要情報を入力後、submitする
- リマインダーコマンドが生成されるので、メッセージとして送信する

## Deploy
### 1.Slack Appを作成
---
- [Slack Apps](https://api.slack.com/apps)から新規アプリを作成
- 「From an app manifest」を選択
- インストールするワークスペースを選択
- 「JSON」を選択肢、manifest.json を入力
- 「Create」を選択

### 2.venv
---
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.環境変数
---
`SLACK_SIGNING_SECRET` 
> App のメニュー -> Basic Information -> App Credentials -> Signing Secret

`SLACK_BOT_TOKEN` 
> App のメニュー -> OAuth & Permissions -> OAuth Tokens for Your Workspace

`SLACK_APP_TOKEN`
> App のメニュー -> Basic Information -> App-Level Tokens -> Tokens

```bash
export SLACK_SIGNING_SECRET=xxxxxxxxxxxxxx
export SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxx-xxxxxxxxxx
export SLACK_APP_TOKEN=xapp-x-xxxxxxxxxxxxx-xxxxxxxxxxxx
```
### 4.aws cli
---
IAM userを発行する
```
AWS Access Key ID:{access key}
AWS Secret Access Key:{secret access key}
Default region name:ap-northeast-1
Default output format:json
```
### 5.serverless-framework
---
```bash
npm install -g serverless
serverless plugin install -n serverless-python-requirements
serverless deploy
```
## Features
入力可能な情報
- リマインドメッセージ
- リマインド送信先
    - 自分自身
    - チャンネル
- (リマインドチャンネル)
- リマインドサイクル
    - 単発
    - 繰り返し
- (繰り返し設定)
    - 毎日
    - 毎週
    - 毎月
    - 毎年
- リマインド時間
    - 時間
    - 日付
    - 曜日

削除やリマインダーの管理はSlackの「後で」メニューから行う

## Reference

https://slack.dev/bolt-python/ja-jp/tutorial/getting-started

https://qiita.com/seratch/items/0b1790697281d4cf6ab3

https://qiita.com/seratch/items/93714b5cf3974c2f5327

https://qiita.com/seratch/items/12b39d636daf8b1e5fbf

https://api.slack.com/reference/block-kit/blocks

https://api.slack.com/reference/block-kit/block-elements