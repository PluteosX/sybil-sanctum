import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HOUR = 'hora'  # The word for 'hour' in Spanish is 'hora'.
HOURS = 'horas'  # The word for 'hours' in Spanish is 'horas'.
DAY = 'día'  # The word for 'day' in Spanish is 'día'.
ONE_STR = '1'
SAME_DAY = 'Same day'
D_LATER = 'd later'

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

CHAIN_INFO_TXT = 'chain_info.txt'
TOP_10_COIN_INFO_TXT = 'top_10_coin_info.txt'
TODAY_COINS_TXT = 'today_coins.txt'
