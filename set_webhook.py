
import requests


def set_webhook():
    our_url = "https://b129-89-36-113-226.ngrok-free.app/telegram"
    telegram_url = f"https://api.telegram.org/bot6821013209:AAH9k_-15JyXqQGK9_2NYAYkabTmyYu97e4/setWebhook"

    data = {
        'url': our_url
    }

    response = requests.post(telegram_url, data=data)

    print(response.json())


if __name__ == '__main__':
    set_webhook()