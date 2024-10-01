from src.constants import HOUR, HOURS, DAY
from src.models.cryptocurrency import Cryptocurrency
from src.utils.coingecko_utils import get_coin_info, get_coins_market_data_info


def get_today_added_coins(coins):
    today_coins = list(filter(_get_today_cryptocurrencies, coins))
    today_added_coins = []

    for coin in today_coins:
        coin_info = get_coin_info(coin.get('id'))
        today_added_coins.append(_cast_to_cryptocurrency(coin, coin_info))

    return today_added_coins


def get_two_weeks_market_data_coins(coins):
    two_weeks_coins = list(filter(_get_two_weeks_cryptocurrencies, coins))
    two_weeks_id_coins = ','.join(list(map(lambda coin: coin['id'], two_weeks_coins)))

    obj = get_coins_market_data_info(two_weeks_id_coins)

    return obj


def _get_today_cryptocurrencies(coin):
    return HOUR in coin['last_added'] or HOURS in coin['last_added']


def _get_two_weeks_cryptocurrencies(coin):
    last_added_array_by_day = coin['last_added'].split(DAY)
    return len(last_added_array_by_day) > 1 and int(last_added_array_by_day[0].strip()) < 16


def _cast_to_cryptocurrency(coin, coin_info):
    return Cryptocurrency(id=coin.get('id'),
                          name=coin.get('name'),
                          price=coin.get('price'),
                          platform=coin_info.get('asset_platform_id'),
                          categories=coin_info.get('categories'),
                          description=coin_info.get('description').get("en"),
                          homepage=coin_info.get('links').get('homepage')[0],
                          blockchain_sites=coin_info.get('links').get('blockchain_site'),
                          additional_notices=coin_info.get('additional_notices'))
