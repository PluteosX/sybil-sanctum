import requests
import time
from bs4 import BeautifulSoup
import re


def get_new_cryptocurrencies_list():
    url = 'https://www.coingecko.com/es/new-cryptocurrencies?items=300'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        coin_table = soup.find_all('tr',
                                   class_='hover:tw-bg-gray-50 tw-bg-white dark:tw-bg-moon-900 hover:dark:tw-bg-moon-800 tw-text-sm')

        new_coins = []

        for coin_item in coin_table:
            id_coin = coin_item.find('a', class_='tw-flex tw-items-center tw-w-full').get('href').split('/')[-1]

            name_coin = \
                re.sub(r'\s+', ' ', coin_item.find('a', class_='tw-flex tw-items-center tw-w-full').text.strip()).strip()

            td_price_coin = coin_item.find('td',
                                           class_='tw-text-end tw-px-1 tw-py-2.5 2lg:tw-p-2.5 tw-bg-inherit tw-text-gray-900 dark:tw-text-moon-50')
            price_coin = td_price_coin.find('span').text.strip()

            last_added = coin_item.find('td',
                                        class_='tw-text-end tw-box-content tw-h-[56px] tw-px-1 tw-py-2.5 2lg:tw-p-2.5 tw-bg-inherit tw-text-gray-900 dark:tw-text-moon-50').text.strip()

            new_coins.append({'id': id_coin, 'name': name_coin, 'price':
                float(price_coin.replace('$', '').replace('.', '').replace(',', '.')), 'last_added': last_added})

    else:
        print(f"Error in the request: {response.status_code}")

    return new_coins


def get_coin_info(id_coin, retries=10, wait_time=30):
    url = f'https://api.coingecko.com/api/v3/coins/{id_coin}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429 and retries > 0:
            print("WARN: Too many requests. Waiting before trying again...")
            time.sleep(wait_time)

            return get_coin_info(id_coin, retries - 1, wait_time * 2)

        else:
            print(f"Error in the request for {id_coin} with status code: {response.status_code}."
                  f"Error: {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Connection error for {id_coin}: {e}")
        return None


def get_coins_market_data_info(id_coins):
    params = {
        'vs_currency': 'usd',
        'ids': id_coins
    }
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets', params=params)
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(f"Error in the request with status code: {response.status_code}."
              f"Error: {e}")
        return None



