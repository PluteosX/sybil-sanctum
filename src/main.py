import json
import pandas as pd

from utils.coingecko_utils import get_new_cryptocurrencies_list
from utils.coin_utils import get_week_market_data_coins, get_today_added_coins


def main():
    new_cryptocurrencies_list = get_new_cryptocurrencies_list()
    # today_coins = get_today_added_coins(new_cryptocurrencies_list)
    week_market_data_coins = get_week_market_data_coins(new_cryptocurrencies_list)

    # fecha = datetime.strptime(coin_market_data_info.get("ath_date"), "%Y-%m-%dT%H:%M:%S.%fZ")
    # Obtener solo la hora
    # hora = fecha.time().hour

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    df = pd.DataFrame(week_market_data_coins)
    df_result =\
        df.groupby('chain')\
            .agg({'higher_price_date': list})\
            .reset_index()

    print(df_result)

    # Escribir el contenido del DataFrame en un archivo de texto
    # with open('dataframe_output.txt', 'w') as f:
    #     f.write(df.to_string())

    # try:
    #     with open('datos.json', 'w') as archivo:
    #         json.dump(week_market_data_coins, archivo, indent=4)
    #     print("Archivo JSON creado con éxito.")
    # except Exception as e:
    #     print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
