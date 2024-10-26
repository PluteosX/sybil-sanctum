from src.constants import CHAINS_INFO_TXT, TOP_10_WEEK_COINS_TXT, TODAY_COINS_TXT


def chain_info_txt_file(data, filename=CHAINS_INFO_TXT):
    with open(filename, 'w', encoding="utf-8") as f:
        for coin in data:
            f.write(f"Chain: {coin['chain']} ({coin['total_count']})\n\n")
            f.write("Cuando se alcanzo el valor maximo (top 3):\n\n")
            for price in coin['higher_price_top_3']:
                f.write(f"- {price[0]}: {price[1]}%\n\n")
            f.write("Cuando se alcanzo el valor minimo (top 3):\n\n")
            for price in coin['lower_price_top_3']:
                f.write(f"- {price[0]}: {price[1]}%\n\n")
            f.write(f"Hora donde se alcanzo el mayor numero de valores maximos: "
                    f"{coin['rank_higher_hours_mode']} ({coin['percentage_rank_higher_hours']}%)\n\n")
            f.write(f"Hora donde se alcanzo el mayor numero de valores minimos: "
                    f"{coin['rank_lower_hours_mode']} ({coin['percentage_rank_lower_hours']}%)\n\n")
            f.write("Mayor porcentaje de subida (Top 3):\n\n")
            for percentage in coin['higher_price_percentage_top_3']:
                f.write(f"- {percentage}%\n\n")
            f.write("Mayor porcentaje de bajada (Top 3):\n\n")
            for percentage in coin['lower_price_percentage_top_3']:
                f.write(f"- {percentage}%\n\n")
            f.write(f"Porcentaje de monedas que nunca superaron su valor inicial:"
                    f"{coin['percentage_never_above_initial_mode']}%\n\n")
            f.write(f"Porcentaje de monedas que nunca bajaron su valor inicial: {coin['percentage_below_initial_mode']}%\n\n")
            f.write(f"-------------------------------------------------------------------------------------------\n\n")


def top_10_coins_txt_file(data, filename=TOP_10_WEEK_COINS_TXT):
    with open(filename, 'w', encoding="utf-8") as f:
        for coin in data:
            f.write(f"Nombre: {coin['name']} ({coin['id']})\n\n")
            f.write(f"Chain: {coin['chain']}\n\n")
            f.write(f"¿Es meme?: {coin['is_meme']}\n\n")
            f.write(f"Descripcion: {coin['description_en']}\n\n")
            f.write(f"Web: {coin['homepage_url']}\n\n")
            f.write(f"Maximo porcentaje de subida: {coin['higher_price_percentage']}%\n\n")
            f.write(f"Cuando alcanzo su valor maximo: {coin['higher_price_date_relation']}\n\n")
            f.write(f"Hora donde alcanzo su valor maximo: {coin['higher_hour']}\n\n")
            f.write(f"Dia de la semana donde alcanzo su valor maximo: {coin['higher_day_week']}\n\n")
            f.write(f"Maximo porcentaje de bajada: {coin['lower_price_percentage']}%\n\n")
            f.write(f"Cuando alcanzo su valor minimo: {coin['lower_price_date_relation']}\n\n")
            f.write(f"Hora donde alcanzo su valor minimo: {coin['lower_hour']}\n\n")
            f.write(f"-------------------------------------------------------------------------------------------\n\n")


def today_coins_txt_file(data, filename=TODAY_COINS_TXT):
    with open(filename, 'w', encoding="utf-8") as f:
        for crypto in data:
            f.write(f"Nombre: {crypto.name} ({crypto.id})\n\n")
            f.write(f"Añadida: {crypto.last_added}\n\n")
            f.write(f"Chain: {crypto.platform}\n\n")
            f.write(f"Descripcion: {crypto.description}\n\n")
            f.write(f"Categorias: {crypto.categories}\n\n")
            f.write(f"Web: {crypto.homepage}\n\n")
            f.write(f"-------------------------------------------------------------------------------------------\n\n")


