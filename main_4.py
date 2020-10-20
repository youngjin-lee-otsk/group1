import json
from flask import Flask, request, make_response
from slacker import Slacker
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread

#슬렉 토큰 가져오기
token = 'xoxb-1438541073680-1464496110944-QWeROmHrY4cIFUqjIl8JC9D4'
slack = Slacker(token)

#플레스크 서버 띄우기
app = Flask(__name__)

#구글 쉬트 및 크리덴셜 정보 가져오기
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:/py/chatBot/group1/butterfly-257608-926179e2b552.json',
    scopes=scope
)

#시트 값들 리스트로 가져오기
gc = gspread.authorize(credentials)
gc1 = gc.open("KYS_ButterflyProject").worksheet('Sample')
gc2 = gc1.get_all_values()

#응답
def get_answer():
    return "뭔말하삼?"

#이벤트 핸들러 호출
def event_handler(event_type, slack_event, val):
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        if val is None:
            text = get_answer()
        else:
            text = val
        slack.chat.post_message(channel, text)
        return make_response("앱 멘션 메세지가 보내졌습니다.", 200, )
    message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

#URI 맞는 라우트 설정
@app.route("/slack", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200,
                            {"content_type": "application/json"})
    for idx, keys in enumerate(gc2):
        if keys[0] in slack_event["event"]["blocks"][0]["elements"][0]["elements"][1]["text"]:
            for idx2, val in enumerate(gc2[idx]):
                if idx2 > 1 :
                    event_type = slack_event["event"]["type"]
                    return event_handler(event_type, slack_event, val)
    for idx, keys in enumerate(gc2):
        if keys[0] not in slack_event["event"]["blocks"][0]["elements"][0]["elements"][1]["text"]:
            event_type = slack_event["event"]["type"]
            return event_handler(event_type, slack_event, None)
        
        # elif "event" in slack_event:
        #     event_type = slack_event["event"]["type"]
        #     val = "none"
        #     return event_handler(event_type, slack_event, val)
        #     return make_response("슬랙 요청에 이벤트 없습니다.", 404,
        #                     {"X-Slack-No-Retry": 1})
    return make_response("슬랙 요청에 이벤트 없습니다.", 404,
                        {"X-Slack-No-Retry": 1})


#기본 라우트
@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World!"

#서버 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)