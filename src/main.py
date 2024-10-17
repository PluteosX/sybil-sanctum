import sys
import os
import numpy as np
import pandas as pd

from src.utils.analytics_utils import get_chain_info, get_top_10_coin_info
from datetime import datetime
from utils.coingecko_utils import get_new_cryptocurrencies_list
from utils.coin_utils import get_week_market_data_coins, get_today_added_coins

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def main():
    new_cryptocurrencies_list = get_new_cryptocurrencies_list()
    # today_coins = get_today_added_coins(new_cryptocurrencies_list)
    week_market_data_coins = get_week_market_data_coins(new_cryptocurrencies_list)

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    df = pd.DataFrame(week_market_data_coins)
    df['creation_day'] = df['creation_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').day)
    df['higher_day'] = df['higher_price_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').day)
    df['higher_hour'] = df['higher_price_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').hour)
    df['lower_day'] = df['lower_price_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').day)
    df['lower_hour'] = df['lower_price_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').hour)

    df_result = (
        df
        .assign(never_above_initial=np.where(
            df['higher_price_percentage'] <= 0, True, False
        ))
        .assign(never_below_initial=np.where(
            df['lower_price_percentage'] <= 0, True, False
        ))
        .assign(higher_price_date_relation=np.where(
            df['higher_day'] == df['creation_day'], 'Same day',
            (df['higher_day'] - df['creation_day']).astype(str) + 'd later'))
        .assign(lower_price_date_relation=np.where(
            df['lower_day'] == df['creation_day'], 'Same day',
            (df['lower_day'] - df['creation_day']).astype(str) + 'd later'))
    )

    rank_higher_hours = df_result['higher_hour'].value_counts()
    rank_lower_hours = df_result['lower_hour'].value_counts()

    df_chain_info = get_chain_info(df_result)

    df_top_10_coins = get_top_10_coin_info(df_result)

    print(df_top_10_coins)

if __name__ == "__main__":
    main()
