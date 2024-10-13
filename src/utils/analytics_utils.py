from src.constants import ONE_STR
from src.utils.statistics_utils import calculate_top_3_mode_with_counts, calculate_mode, calculate_top_3_highest


def _is_not_yesterday_cryptocurrency(row):
    return ONE_STR not in row['last_added']


def get_chain_info(df):
    df_chain_info = (
        df
        .loc[df.apply(_is_not_yesterday_cryptocurrency, axis=1)]  # Exclude coins launched yesterday to avoid
                                                                  # distorting the results with 'Same day' values.
        .groupby('chain')
        .agg(
            total_count=('chain', 'count'),
            higher_price_top_3=('higher_price_date_relation', calculate_top_3_mode_with_counts),
            lower_price_top_3=('lower_price_date_relation', calculate_top_3_mode_with_counts),
            count_never_above_initial_mode=('never_above_initial', lambda x: (x == True).sum()),
            count_never_below_initial_mode=('never_below_initial', lambda x: (x == True).sum()),
            rank_higher_hours_mode=('higher_hour', calculate_mode),
            count_rank_higher_hours=('higher_hour', lambda x: (x == calculate_mode(x)).sum()),
            rank_lower_hours_mode=('lower_hour', calculate_mode),
            count_rank_lower_hours=('lower_hour', lambda x: (x == calculate_mode(x)).sum()),
            higher_price_percentage_top_3=('higher_price_percentage', calculate_top_3_highest),
            lower_price_percentage_top_3=('lower_price_percentage', calculate_top_3_highest)
        )
        .reset_index()
    )

    return df_chain_info
