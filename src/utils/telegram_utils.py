import requests

from src.constants import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_message(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    with open(file_path, 'rb') as f:
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID}, files={'document': f})