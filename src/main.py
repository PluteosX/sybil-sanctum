from utils.coingecko_utils import get_new_cryptocurrencies_list
from utils.coin_utils import get_two_weeks_market_data_coins


def main():
    new_coins = get_two_weeks_market_data_coins(get_new_cryptocurrencies_list())

    print(new_coins)

if __name__ == "__main__":
    main()
