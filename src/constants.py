import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HOUR = 'hora'  # The word for 'hour' in Spanish is 'hora'.
HOURS = 'horas'  # The word for 'hours' in Spanish is 'horas'.
MINUTE = 'minuto'  # The word for 'minute' in Spanish is 'minuto'.
MINUTES = 'minutos'  # The word for 'minutes' in Spanish is 'minutos'.
DAY = 'día'  # The word for 'day' in Spanish is 'día'.
ONE_STR = '1'
SAME_DAY = 'Same day'
D_LATER = 'd later'

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

CHAINS_INFO = 'chains_info'
TOP_10_WEEK_COINS = 'top_10_week_coins'
TODAY_COINS = 'today_coins'
LAST_HALF_HOUR_COINS = 'last_half_hour_coins'

CHAINS_INFO_TXT = 'chains_info.txt'
TOP_10_WEEK_COINS_TXT = 'top_10_week_coins.txt'
TODAY_COINS_TXT = 'today_coins.txt'
