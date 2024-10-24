import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.constants import CHAIN_INFO_TXT, TOP_10_COIN_INFO_TXT, TODAY_COINS_TXT
from src.utils.file_utils import chain_info_txt_file, top_10_coins_txt_file, today_coins_txt_file
from src.utils.telegram_utils import send_message
from src.utils.analytics_utils import get_chain_info, get_top_10_coin_info, get_week_coins_df
from utils.coingecko_utils import get_new_cryptocurrencies_list
from utils.coin_utils import get_week_market_data_coins, get_today_added_coins


def main():
    new_cryptocurrencies_list = get_new_cryptocurrencies_list()
    today_coins = get_today_added_coins(new_cryptocurrencies_list)
    week_market_data_coins = get_week_market_data_coins(new_cryptocurrencies_list)

    df_week_coins = get_week_coins_df(week_market_data_coins)

    df_chain_info = get_chain_info(df_week_coins)
    chain_info_txt_file(df_chain_info.to_dict(orient='records'))
    send_message(CHAIN_INFO_TXT)

    df_top_10_coins = get_top_10_coin_info(df_week_coins)
    top_10_coins_txt_file(df_top_10_coins.to_dict(orient='records'))
    send_message(TOP_10_COIN_INFO_TXT)

    today_coins_txt_file(today_coins)
    send_message(TODAY_COINS_TXT)


if __name__ == "__main__":
    main()
