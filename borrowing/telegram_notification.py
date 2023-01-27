import requests


def borrowing_telegram_notification(text: str, chat: str, token: str):
    url_request = (
        f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={text}"
    )

    result = requests.get(url_request)

    return result.json()
