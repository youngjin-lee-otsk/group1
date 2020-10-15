import requests
"""Simon Test"""
def main():
    # webhook url
    url = "https://hooks.slack.com/services/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"

    text = "꺼져"

    payload = {
        "text": text
    }

    requests.post(url, json=payload)

# 이 스크립트에서 실행할 함수는 main
if __name__ == "__main__":
    main()