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


def get_week_market_data_coins(coins):
    week_coins = list(filter(_get_week_cryptocurrencies, coins))
    week_id_coins = ','.join(list(map(lambda coin: coin['id'], week_coins)))

    coins_market_data_info = get_coins_market_data_info(week_id_coins)

    new_coins = []

    for coin in week_coins:
        coin_market_data_info = next((c for c in coins_market_data_info
                                      if c['id'] == coin.get('id')), None)

        initial_price = coin_market_data_info.get("sparkline_in_7d").get("price")[0]

        new_coins.append(dict(
            id=coin.get("id"),
            name=coin.get("name"),
            last_added=coin.get("last_added"),
            creation_date=coin.get("creation_date").strftime('%Y-%m-%d'),
            chain=coin.get("chain"),
            initial_price=initial_price,
            current_price=coin.get("price"),
            # Percentage relative to the opening price
            current_price_percentage=((coin.get("price") - initial_price) / initial_price) * 100,
            higher_price=coin_market_data_info.get("ath"),
            # Percentage relative to the opening price
            higher_price_percentage=((coin_market_data_info.get("ath") - initial_price) / initial_price) * 100,
            higher_price_date=coin_market_data_info.get("ath_date"),
            lower_price=coin_market_data_info.get("atl"),
            # Percentage relative to the opening price
            lower_price_percentage=((initial_price - coin_market_data_info.get("atl")) / initial_price) * 100,
            lower_price_date=coin_market_data_info.get("atl_date"),
            price_change_percentage_24h=coin_market_data_info.get("price_change_percentage_24h_in_currency")
        ))


    return new_coins


def _get_today_cryptocurrencies(coin):
    return HOUR in coin['last_added'] or HOURS in coin['last_added']


def _get_week_cryptocurrencies(coin):
    last_added_array_by_day = coin['last_added'].split(DAY)
    return len(last_added_array_by_day) > 1 and int(last_added_array_by_day[0].strip()) < 8


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
