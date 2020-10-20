import os
import slack

slack_token = 'xoxb-1438541073680-1411752179141-d6eH4TXrId5nm48G8smuYqwh'

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    
    # if 'text' in data and 'Hello' in data.get('text', []):
    # if 'Hello' in data.get('text', ''):
    if 'Hello' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            # thread_ts=thread_ts
        )

if __name__ == '__main__':
    client = slack.WebClient(token=slack_token)
    response = client.chat_postMessage(
        channel='#test',
        text="ediBot is now ready!")
    bot_token = 'xoxb-1438541073680-1411752179141-d6eH4TXrId5nm48G8smuYqwh'
    rtm_client = slack.RTMClient(token=bot_token, ssl=False)
    rtm_client.start()
