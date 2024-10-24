from src.constants import CHAIN_INFO_TXT, TOP_10_COIN_INFO_TXT, TODAY_COINS_TXT


def chain_info_txt_file(data, filename=CHAIN_INFO_TXT):
    with open(filename, 'w') as f:
        for coin in data:
            f.write(f"Chain: {coin['chain']} ({coin['total_count']})\n")
            f.write("Cuando se alcanzo el valor maximo (top 3):\n")
            for price in coin['higher_price_top_3']:
                f.write(f"- {price[0]}: {price[1]}%\n")
            f.write("Cuando se alcanzo el valor minimo (top 3):\n")
            for price in coin['lower_price_top_3']:
                f.write(f"- {price[0]}: {price[1]}%\n")
            f.write(f"Hora donde se alcanzo el mayor numero de valores maximos: "
                    f"{coin['rank_higher_hours_mode']} ({coin['percentage_rank_higher_hours']}%)\n")
            f.write(f"Hora donde se alcanzo el mayor numero de valores minimos: "
                    f"{coin['rank_lower_hours_mode']} ({coin['percentage_rank_lower_hours']}%)\n")
            f.write("Mayor % de subida (Top 3):\n")
            for percentage in coin['higher_price_percentage_top_3']:
                f.write(f"- {percentage}%\n")
            f.write("Mayor % de bajada (Top 3):\n")
            for percentage in coin['lower_price_percentage_top_3']:
                f.write(f"- {percentage}%\n")
            f.write(f"% de monedas que nunca superaron su valor inicial:"
                    f"{coin['percentage_never_above_initial_mode']}%\n")
            f.write(f"% de monedas que nunca bajaron su valor inicial: {coin['percentage_below_initial_mode']}%\n\n")
            f.write(f"-------------------------------------------------------------------------------------------\n\n")


def top_10_coins_txt_file(data, filename=TOP_10_COIN_INFO_TXT):
    with open(filename, 'w') as f:
        for coin in data:
            f.write(f"Nombre: {coin['name']} ({coin['id']})\n")
            f.write(f"Chain: {coin['chain']}\n")
            f.write(f"¿Es meme?: {coin['is_meme']}\n")
            f.write(f"Descripcion: {coin['description_en']}\n")
            f.write(f"Web: {coin['homepage_url']}\n")
            f.write(f"Maximo % de subida: {coin['higher_price_percentage']}%\n")
            f.write(f"Cuando alcanzo su valor maximo: {coin['higher_price_date_relation']}\n")
            f.write(f"Hora donde alcanzo su valor maximo: {coin['higher_hour']}\n")
            f.write(f"Dia de la semana donde alcanzo su valor maximo: {coin['higher_day_week']}\n\n")
            f.write(f"-------------------------------------------------------------------------------------------\n\n")


def today_coins_txt_file(data, filename=TODAY_COINS_TXT):
    with open(filename, 'w') as f:
        for crypto in data:
            f.write(f"Nombre: {crypto.name} ({crypto.id})\n")
            f.write(f"Añadida: {crypto.last_added}\n")
            f.write(f"Chain: {crypto.platform}\n")
            f.write(f"Descripcion: {crypto.description}\n")
            f.write(f"Categorias: {crypto.categories}\n")
            f.write(f"Web: {crypto.homepage}\n")
            f.write(f"Noticias adicionales: {crypto.additional_notices}\n\n")
            f.write(f"-------------------------------------------------------------------------------------------\n\n")


