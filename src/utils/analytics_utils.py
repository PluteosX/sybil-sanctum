import calendar
from datetime import datetime

import numpy as np
import pandas as pd

from src.constants import ONE_STR, SAME_DAY, D_LATER, DATE_FORMAT, DATETIME_FORMAT
from src.utils.coingecko_utils import get_coin_info
from src.utils.statistics_utils import calculate_top_3_mode_with_percentage, calculate_mode, calculate_top_3_highest, \
    calculate_percentage


def get_week_coins_df(week_coins_list):
    df = pd.DataFrame(week_coins_list)
    df['creation_day'] = df['creation_date'].apply(lambda x: datetime.strptime(x, DATE_FORMAT).day)
    df['higher_day'] = df['higher_price_date'].apply(lambda x: datetime.strptime(x, DATETIME_FORMAT).day)
    df['higher_hour'] = df['higher_price_date'].apply(lambda x: datetime.strptime(x, DATETIME_FORMAT).hour)
    df['lower_day'] = df['lower_price_date'].apply(lambda x: datetime.strptime(x, DATETIME_FORMAT).day)
    df['lower_hour'] = df['lower_price_date'].apply(lambda x: datetime.strptime(x, DATETIME_FORMAT).hour)

    df_result = (
        df
        .assign(never_above_initial=np.where(
            df['higher_price_percentage'] <= 0, True, False
        ))
        .assign(never_below_initial=np.where(
            df['lower_price_percentage'] <= 0, True, False
        ))
        .assign(higher_price_date_relation=np.where(
            df['higher_day'] == df['creation_day'], SAME_DAY,
            (df['higher_day'] - df['creation_day']).astype(str) + D_LATER))
        .assign(lower_price_date_relation=np.where(
            df['lower_day'] == df['creation_day'], SAME_DAY,
            (df['lower_day'] - df['creation_day']).astype(str) + D_LATER))
    )

    return df_result


def get_chain_info(df):
    df_chain_info = (
        df
        # Exclude coins launched yesterday to avoid distorting the results with 'Same day' values.
        .loc[df.apply(_is_not_yesterday_cryptocurrency, axis=1)]
        .groupby('chain')
        .agg(
            total_count=('chain', 'count'),
            # Not very reliable, recently added coins interfere a lot. TODO: review
            higher_price_top_3=('higher_price_date_relation',
                                lambda x: calculate_top_3_mode_with_percentage(x, len(x))),
            # Not very reliable, recently added coins interfere a lot. TODO: review
            lower_price_top_3=('lower_price_date_relation',
                               lambda x: calculate_top_3_mode_with_percentage(x, len(x))),
            count_never_above_initial_mode=('never_above_initial', lambda x: (x == True).sum()),
            count_never_below_initial_mode=('never_below_initial', lambda x: (x == True).sum()),
            rank_higher_hours_mode=('higher_hour', calculate_mode),
            count_rank_higher_hours=('higher_hour', lambda x: (x == calculate_mode(x)).sum()),
            rank_lower_hours_mode=('lower_hour', calculate_mode),
            count_rank_lower_hours=('lower_hour', lambda x: (x == calculate_mode(x)).sum()),
            higher_price_percentage_top_3=('higher_price_percentage', calculate_top_3_highest),
            lower_price_percentage_top_3=('lower_price_percentage', calculate_top_3_highest),
            total_higher_price_percentage=('higher_price_percentage', 'sum'),
            total_lower_price_percentage=('lower_price_percentage', 'sum')
        )
        .reset_index()
    )

    df_chain_info['percentage_never_above_initial_mode'] =\
        calculate_percentage(df_chain_info, 'count_never_above_initial_mode', 'total_count')
    df_chain_info['percentage_below_initial_mode'] = \
        calculate_percentage(df_chain_info, 'count_never_below_initial_mode', 'total_count')
    df_chain_info['percentage_rank_higher_hours'] = \
        calculate_percentage(df_chain_info, 'count_rank_higher_hours', 'total_count')
    df_chain_info['percentage_rank_lower_hours'] = \
        calculate_percentage(df_chain_info, 'count_rank_lower_hours', 'total_count')
    df_chain_info['higher_minus_lower_price_percentage'] =\
        df_chain_info['total_higher_price_percentage'] - df_chain_info['total_lower_price_percentage']

    df_chain_info_sorted = df_chain_info.sort_values(by='higher_minus_lower_price_percentage', ascending=False)

    return df_chain_info_sorted[['chain', 'total_count', 'higher_price_top_3', 'lower_price_top_3',
                                 'rank_higher_hours_mode', 'percentage_rank_higher_hours', 'rank_lower_hours_mode',
                                 'percentage_rank_lower_hours', 'higher_price_percentage_top_3',
                                 'lower_price_percentage_top_3', 'percentage_never_above_initial_mode',
                                 'percentage_below_initial_mode']]


def get_top_10_coin_info(df):

    df_10 = df.nlargest(10, 'higher_price_percentage')
    df_10['higher_day_week'] = df_10['higher_price_date'] \
        .apply(lambda x: calendar.day_name[datetime.strptime(x, DATETIME_FORMAT).weekday()])

    df_coin_top_10 = df_10[['id', 'chain', 'higher_price_percentage', 'higher_price_date_relation',
                            'higher_hour', 'higher_day_week']]

    ids = df_coin_top_10['id'].tolist()

    coin_info_top_10_list = []
    for id in ids:
        coin_info = get_coin_info(id)
        coin_info_top_10_list.append(coin_info)

    df_coin_info_top_10 = pd.DataFrame(coin_info_top_10_list)
    df_merged = pd.merge(left=df_coin_top_10, right=df_coin_info_top_10, how='left', on='id')
    df_merged['is_meme'] = df_merged['categories'].apply(lambda x: 'Meme' in x)
    df_merged['homepage_url'] = df_merged['links'].apply(lambda x: x['homepage'][0] if x['homepage'] else None)
    df_merged['description_en'] = df_merged['description'].apply(lambda x: x['en'])

    return df_merged[['id', 'name', 'chain', 'description_en', 'homepage_url', 'is_meme', 'higher_price_percentage',
                      'higher_price_date_relation', 'higher_hour', 'higher_day_week']]


def _is_not_yesterday_cryptocurrency(row):
    return ONE_STR not in row['last_added']