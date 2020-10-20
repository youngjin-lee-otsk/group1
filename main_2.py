import requests
"""Simon Test 22"""
def main():
    # webhook url
    url = "https://hooks.slack.com/services/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"

    text = "안녕~기택!"

    payload = {
        "text": text
    }

    requests.post(url, json=payload)

# 이 스크립트에서 실행할 함수는 main
if __name__ == "__main__":
    main()