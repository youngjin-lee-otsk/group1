import json
from flask import Flask, request, make_response
from slacker import Slacker
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread
import random
import pyowm

#슬렉 토큰 가져오기
token = 'xoxb-1438541073680-1411752179141-X7geaTcVXJbOFgRPyydcZ0bQ'
slack = Slacker(token)

#pyowm 을 통해 날씨 정보 가져오자
API_Key = '2738e08dc88598ebd27bf2355a1680eb'
owm = pyowm.OWM(API_Key)
 
City_ID = 1835848
manager = owm.weather_manager()
obs = manager.weather_at_id(City_ID)
City_name = obs.location.name
Temp = obs.weather.temperature(unit='celsius')
Status = obs.weather.status

w_comment = ('도시명은 ' + City_name + ' 입니다.\n'
+ City_name + '의 최고기온은 ' + str(Temp['temp_max']) + ' 도 입니다.\n'
+ City_name + '의 최저기온은 ' + str(Temp['temp_min']) + ' 도 입니다.\n'
+ City_name + '의 현재기온은 ' + str(Temp['temp']) + ' 도 입니다.\n'
+ City_name + '의 현재날씨는 ' + Status + ' 입니다.'
)

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

#구글 시트 매칭키값 없을시 응답
def get_answer():
    return "뭔말하삼?"

#이벤트 핸들러 호출, 구글 시트 매칭값 있을시 호출
def event_handler(event_type, slack_event, val):
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        if val is None:
            text = get_answer()
        else:
            text = val
        print(text)
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

    event_type = slack_event["event"]["type"]
    totalArray = []
    sumArray = []
    for idx, keys in enumerate(gc2):
        if keys[0] in slack_event["event"]["blocks"][0]["elements"][0]["elements"][1]["text"]:
            totalArray.append(keys[0])
            for idx2, val in enumerate(gc2[idx]):
                if idx2 > 1 :
                    sumArray.append(val)
            totalArray.append(sumArray)

    if totalArray != []:
        finalValue = random.sample(totalArray[1], 1)
        if totalArray[0] == 'weather':
            return event_handler(event_type, slack_event, w_comment)
        else:
            return event_handler(event_type, slack_event, finalValue)
    else:
        return event_handler(event_type, slack_event, None)
    return make_response("슬랙 요청에 이벤트 없습니다.", 404,
                        {"X-Slack-No-Retry": 1})


#기본 라우트
@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World!"

#서버 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)