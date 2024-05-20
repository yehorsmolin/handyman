import requests


def send_message(chat_id, text):
    telegram_url = f'https://api.telegram.org/bot6821013209:AAH9k_-15JyXqQGK9_2NYAYkabTmyYu97e4/sendMessage'

    data = {
        'chat_id': chat_id,
        'text': text
    }

    response = requests.post(telegram_url, data=data)
    print(response.json())


if __name__ == '__main__':
    chat_id = 378999070
    text = "How are you?"
    send_message(chat_id, text)
