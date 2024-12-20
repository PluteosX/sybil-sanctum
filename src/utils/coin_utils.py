from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.constants import HOUR, HOURS, DAY, DATE_FORMAT, MINUTE, MINUTES, TODAY_COINS, LAST_HALF_HOUR_COINS
from src.models.cryptocurrency import Cryptocurrency
from src.utils.coingecko_utils import get_coin_info, get_coins_market_data_info


def get_added_coins(coins, type):
    if type == TODAY_COINS:
        filtered_coins = list(filter(_get_today_cryptocurrencies, coins))
    elif type == LAST_HALF_HOUR_COINS:
        filtered_coins = list(filter(_get_last_half_hour_cryptocurrencies, coins))
    else:
        filtered_coins = []

    added_coins = []

    for coin in filtered_coins:
        coin_info = get_coin_info(coin.get("id"))
        added_coins.append(_cast_to_cryptocurrency(coin, coin_info))

    return added_coins


def get_week_market_data_coins(coins):
    week_coins = list(filter(_get_week_cryptocurrencies, coins))
    week_id_coins = ",".join(list(map(lambda coin: coin["id"], week_coins)))

    coins_market_data_info = get_coins_market_data_info(week_id_coins)

    new_coins = []

    for coin in week_coins:
        try:
            coin_market_data_info = next((c for c in coins_market_data_info
                                          if c["id"] == coin.get("id")), None)

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
                higher_price_percentage=np.round(
                    ((coin_market_data_info.get("ath") - initial_price) / initial_price) * 100),
                higher_price_date=coin_market_data_info.get("ath_date"),
                lower_price=coin_market_data_info.get("atl"),
                # Percentage relative to the opening price
                lower_price_percentage=np.round(
                    ((initial_price - coin_market_data_info.get("atl")) / initial_price) * 100),
                lower_price_date=coin_market_data_info.get("atl_date"),
                price_change_percentage_24h=coin_market_data_info.get("price_change_percentage_24h_in_currency")
            ))
        except:
            print(f'WARN: coin {coin.get("id")} can\'t be included due to lack of data in the required parameters.')

    return new_coins


def get_last_half_hour_cryptocurrencies_from_geckoterminal(data, network):
    df = pd.DataFrame(data)
    df["id"] = df["id"].replace(f"{network}_", "", regex=True)
    df["name"] = df["attributes"].apply(lambda x: x["name"])
    df["created_at"] = pd.to_datetime(df["attributes"].apply(lambda x: x["pool_created_at"])) \
                           .dt.tz_localize(None) + timedelta(hours=1)
    df["minutes_since_creation"] = (datetime.now() - df["created_at"]).dt.total_seconds() / 60
    df["minutes_since_creation"] = df["minutes_since_creation"].astype(int)
    df["minutes_since_creation"] = np.where(df["minutes_since_creation"] < 0, 60 + df["minutes_since_creation"],
                                            df["minutes_since_creation"])
    df["fdv"] = df["attributes"].apply(lambda x: x["fdv_usd"]).astype(float)
    df["price_change_percentage"] = df["attributes"].apply(lambda x: x["price_change_percentage"]) \
        .apply(lambda x: x["m5"])
    df["volume"] = df["attributes"].apply(lambda x: x["volume_usd"]).apply(lambda x: x["m5"]).astype(float)
    df["price"] = df["attributes"].apply(lambda x: x["base_token_price_usd"])
    df["contract"] = df["relationships"].apply(lambda x: x["base_token"]) \
        .apply(lambda x: x["data"]).apply(lambda x: x["id"]).replace(f"{network}_", "", regex=True)
    df["url"] = f"https://www.geckoterminal.com/{network}/pools/" + df["contract"]
    df["transactions_buy"] = df["attributes"].apply(lambda x: x["transactions"]) \
        .apply(lambda x: x["m5"]).apply(lambda x: x["buys"])
    df["transactions_sell"] = df["attributes"].apply(lambda x: x["transactions"]) \
        .apply(lambda x: x["m5"]).apply(lambda x: x["sells"])

    df_volume_higher_100k = df[df["volume"] > 100000]

    df_volume_higher_100k.loc[:, "volume"] = df_volume_higher_100k["volume"].apply(lambda x: f"${x:,.2f}")
    df_volume_higher_100k.loc[:, "fdv"] = df_volume_higher_100k["fdv"].apply(lambda x: f"${x:,.2f}")

    return df_volume_higher_100k[["id", "name", "created_at", "minutes_since_creation", "price", "contract", "url",
                                  "fdv", "price_change_percentage", "volume", "transactions_buy",
                                  "transactions_sell"]].to_dict(orient="records")


def _get_today_cryptocurrencies(coin):
    return HOUR in coin["last_added"] or HOURS in coin["last_added"] or \
        MINUTE in coin["last_added"] or MINUTES in coin["last_added"]


def _get_week_cryptocurrencies(coin):
    last_added_array_by_day = coin["last_added"].split(DAY)
    return len(last_added_array_by_day) > 1 and int(last_added_array_by_day[0].strip()) < 8


def _get_last_half_hour_cryptocurrencies(coin):
    last_added_array_by_half_hour = coin["last_added"].split(MINUTE)
    return len(last_added_array_by_half_hour) > 1 and int(last_added_array_by_half_hour[0].strip()) < 31


def _cast_to_cryptocurrency(coin, coin_info):
    asset_platform_id = coin_info.get("asset_platform_id")
    contract = None if coin_info.get("detail_platforms") \
                           .get(asset_platform_id) is None else coin_info.get("detail_platforms") \
        .get(asset_platform_id).get("contract_address")

    return Cryptocurrency(id=coin.get("id"),
                          name=coin.get("name"),
                          price=coin.get("price"),
                          platform=asset_platform_id,
                          contract=contract,
                          categories=coin_info.get("categories"),
                          description=coin_info.get("description").get("en"),
                          homepage=coin_info.get("links").get("homepage")[0],
                          blockchain_sites=coin_info.get("links").get("blockchain_site"),
                          additional_notices=coin_info.get("additional_notices"),
                          last_added=coin.get("last_added"))
