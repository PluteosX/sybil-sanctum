import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import CHAINS_INFO_TXT, TOP_10_WEEK_COINS_TXT, TODAY_COINS_TXT, CHAINS_INFO, TOP_10_WEEK_COINS, \
    TODAY_COINS, LAST_HALF_HOUR_COINS, PLATFORM, COINGECKO, GECKOTERMINAL, NETWORK
from utils.analytics_utils import get_chain_info, get_top_10_coin_info, get_week_coins_df
from utils.coin_utils import get_week_market_data_coins, get_added_coins, \
    get_last_half_hour_cryptocurrencies_from_geckoterminal
from utils.coingecko_utils import get_new_cryptocurrencies_list
from utils.geckoterminal_utils import get_latest_pools_network
from utils.file_utils import chain_info_txt_file, top_10_coins_txt_file, today_coins_txt_file
from utils.message_utils import send_last_half_hour_coins_message
from utils.telegram_utils import send_message_file


def main():
    parser = argparse.ArgumentParser(description="Generate specific cryptocurrency reports")
    parser.add_argument("--generate", choices=[CHAINS_INFO, TOP_10_WEEK_COINS, TODAY_COINS, LAST_HALF_HOUR_COINS],
                        required=True, help="Specify which file to generate")
    args = parser.parse_args()

    new_cryptocurrencies = get_new_cryptocurrencies_list() if PLATFORM == COINGECKO \
        else get_latest_pools_network(NETWORK)

    if args.generate == LAST_HALF_HOUR_COINS:
        if PLATFORM == COINGECKO:
            last_half_hour_coins = get_added_coins(new_cryptocurrencies, LAST_HALF_HOUR_COINS)
        elif PLATFORM == GECKOTERMINAL:
            last_half_hour_coins = get_last_half_hour_cryptocurrencies_from_geckoterminal(new_cryptocurrencies, NETWORK)
        else:
            last_half_hour_coins = []
        send_last_half_hour_coins_message(last_half_hour_coins, PLATFORM)

    else:
        week_market_data_coins = get_week_market_data_coins(new_cryptocurrencies)
        df_week_coins = get_week_coins_df(week_market_data_coins)

        if args.generate == CHAINS_INFO:
            df_chain_info = get_chain_info(df_week_coins)
            chain_info_txt_file(df_chain_info.to_dict(orient='records'))
            send_message_file(CHAINS_INFO_TXT)
        elif args.generate == TOP_10_WEEK_COINS:
            df_top_10_coins = get_top_10_coin_info(df_week_coins)
            top_10_coins_txt_file(df_top_10_coins.to_dict(orient='records'))
            send_message_file(TOP_10_WEEK_COINS_TXT)
        elif args.generate == TODAY_COINS:
            today_coins = get_added_coins(new_cryptocurrencies, TODAY_COINS)
            today_coins_txt_file(today_coins)
            send_message_file(TODAY_COINS_TXT)


if __name__ == "__main__":
    main()
