import os
import json
from flask import Flask, request, make_response
from slacker import Slacker
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread
import random
import pyowm
import requests
from pandas.io.json import json_normalize

#슬렉 토큰 가져오기
# json_slack_path = "C:/Python/slack_butterflt_token.json"
# with open(json_slack_path,'r') as json_file:
#     slack_dict = json.load(json_file)

# slack_token = slack_dict['token']
slack_token = 'xoxb-1438541073680-1496051568912-bq0u8ZUWmeObExA81p3HYL7s'

#token = os.getenv('SLACK_TOKEN', 'nono')
#slack = Slacker(token)

# 채널 이름
ChannelName = "test2"

# 채널 조회 API 메소드: conversations.list
URL = 'https://slack.com/api/conversations.list'

# 파라미터
params = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'token': slack_token
          }

# API 호출
res = requests.get(URL, params = params)

channel_list = json_normalize(res.json()['channels'])
channel_id = list(channel_list.loc[channel_list['name'] == ChannelName, 'id'])[0]

print(f"""
채널 이름: {ChannelName}
채널 id: {channel_id}
""")

# 글 내용
Text = "Butterfly bot test"

# 채널 내 문구 조회 API 메소드: conversations.list
URL = 'https://slack.com/api/conversations.history'

# 파라미터
params = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'token': slack_token,
    'channel': channel_id
         }

# API 호출
res = requests.get(URL, params = params)    

chat_data = json_normalize(res.json()['messages'])
chat_data['text'] = chat_data['text'].apply(lambda x: x.replace("\xa0"," "))
ts = chat_data.loc[chat_data['text'] == Text, 'ts'].to_list()[0]

print(f"""
글 내용: {Text}
ts: {ts}
""")

# Bot으로 등록할 댓글 메시지 문구
message = f"""
Hi, this is Kitaek
"""

# 파라미터
data = {'Content-Type': 'application/x-www-form-urlencoded',
        'token': slack_token,
        'channel': channel_id, 
        'text': message,
        'reply_broadcast': 'True', 
        'thread_ts': ts
        } 

# 메시지 등록 API 메소드: chat.postMessage
URL = "https://slack.com/api/chat.postMessage"
res = requests.post(URL, data=data)