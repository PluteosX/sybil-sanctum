from datetime import time

import requests


def get_latest_pools_network(network, page=1, pages=10, retries=20, wait_time=30):
    data = []

    for page in range(page, pages+1):
        url = f"https://api.geckoterminal.com/api/v2/networks/{network}/new_pools?page={page}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data.extend(response.json()['data'])

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429 and retries > 0:
                print("WARN: Too many requests. Waiting before trying again...")
                time.sleep(wait_time)
                return get_latest_pools_network(network, page=page, pages=page-pages+1,
                                                retries=retries-1, wait_time=wait_time*2)
            else:

                print(f"Error in the request with status code: {response.status_code}."

                      f"Error: {e}")

                return None

    return data
