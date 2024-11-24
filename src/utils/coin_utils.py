import numpy as np

from src.constants import HOUR, HOURS, DAY, DATE_FORMAT, MINUTE, MINUTES, TODAY_COINS, LAST_HOUR_COINS
from src.models.cryptocurrency import Cryptocurrency
from src.utils.coingecko_utils import get_coin_info, get_coins_market_data_info


def get_added_coins(coins, type):
    if type == TODAY_COINS:
        filtered_coins = list(filter(_get_today_cryptocurrencies, coins))
    elif type == LAST_HOUR_COINS:
        filtered_coins = list(filter(_get_last_hour_cryptocurrencies, coins))
    else:
        filtered_coins = []

    added_coins = []

    for coin in filtered_coins:
        coin_info = get_coin_info(coin.get('id'))
        added_coins.append(_cast_to_cryptocurrency(coin, coin_info))

    return added_coins


def get_week_market_data_coins(coins):
    week_coins = list(filter(_get_week_cryptocurrencies, coins))
    week_id_coins = ','.join(list(map(lambda coin: coin['id'], week_coins)))

    coins_market_data_info = get_coins_market_data_info(week_id_coins)

    new_coins = []

    for coin in week_coins:
        try:
            coin_market_data_info = next((c for c in coins_market_data_info
                                          if c['id'] == coin.get('id')), None)

            initial_price = coin_market_data_info.get("sparkline_in_7d").get("price")[0]

            new_coins.append(dict(
                id=coin.get("id"),
                name=coin.get("name"),
                last_added=coin.get("last_added"),
                creation_date=coin.get("creation_date").strftime(DATE_FORMAT),
                chain=coin.get("chain"),
                initial_price=initial_price,
                current_price=coin.get("price"),
                # Percentage relative to the opening price
                current_price_percentage=np.round(((coin.get("price") - initial_price) / initial_price) * 100),
                higher_price=coin_market_data_info.get("ath"),
                # Percentage relative to the opening price
                higher_price_percentage=np.round(((coin_market_data_info.get("ath") - initial_price) / initial_price) * 100),
                higher_price_date=coin_market_data_info.get("ath_date"),
                lower_price=coin_market_data_info.get("atl"),
                # Percentage relative to the opening price
                lower_price_percentage=np.round(((initial_price - coin_market_data_info.get("atl")) / initial_price) * 100),
                lower_price_date=coin_market_data_info.get("atl_date"),
                price_change_percentage_24h=coin_market_data_info.get("price_change_percentage_24h_in_currency")
            ))
        except:
            print(f'WARN: coin {coin.get("id")} can\'t be included due to lack of data in the required parameters.')

    return new_coins


def _get_today_cryptocurrencies(coin):
    return HOUR in coin['last_added'] or HOURS in coin['last_added'] or \
        MINUTE in coin['last_added'] or MINUTES in coin['last_added']


def _get_week_cryptocurrencies(coin):
    last_added_array_by_day = coin['last_added'].split(DAY)
    return len(last_added_array_by_day) > 1 and int(last_added_array_by_day[0].strip()) < 8


def _get_last_hour_cryptocurrencies(coin):
    #return MINUTE in coin['last_added'] or MINUTES in coin['last_added']
    return "alrededor de 6 horas" in coin['last_added']


def _cast_to_cryptocurrency(coin, coin_info):
    return Cryptocurrency(id=coin.get('id'),
                          name=coin.get('name'),
                          price=coin.get('price'),
                          platform=coin_info.get('asset_platform_id'),
                          categories=coin_info.get('categories'),
                          description=coin_info.get('description').get("en"),
                          homepage=coin_info.get('links').get('homepage')[0],
                          blockchain_sites=coin_info.get('links').get('blockchain_site'),
                          additional_notices=coin_info.get('additional_notices'),
                          last_added=coin.get('last_added'))
