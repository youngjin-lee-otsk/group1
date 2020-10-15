import json
import requests
from pandas.io.json import json_normalize

# json_slack_path = "./token.json"
# with open(json_slack_path,'r') as json_file:
#     slack_dict = json.load(json_file)
# webhookUrl = "https://hooks.slack.com/services/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"
slack_token = "xoxb-1438541073680-1411752179141-YhwYs4aqVD1Wmnh7xnv2bSYw"


ChannelName = "test"

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
Text = "슬랙 봇 테스트"

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

# 기택님 너무 멋있어.

# Bot으로 등록할 댓글 메시지 문구
message = f"""
파이썬으로 보내는 테스트 입니다. 아자아자 Group1 화이팅!!
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
