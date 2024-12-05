import textwrap

from src.constants import COINGECKO, GECKOTERMINAL
from src.utils.telegram_utils import send_message_text


def send_last_half_hour_coins_message(coins, platform):
    if len(coins) > 0:
        if platform == COINGECKO:
            send_message_text("<b>🚀 NEW COINS: </b>")
            for crypto in coins:
                message = textwrap.dedent(f"""
                    <b>🪙 {crypto.name}</b>
                    <i>Platform:</i> {crypto.platform}
                    <i>Contract:</i> {crypto.contract}
                    <i>Price:</i> ${crypto.price}
                    <i>Categories:</i> {", ".join(crypto.categories)}
                    <i>Description:</i> {crypto.description}
                    <a href="{crypto.homepage}">🔗 Homepage</a>
                    <i>Last added:</i> {crypto.last_added}
                    """).strip()
                send_message_text(message)
        elif platform == GECKOTERMINAL:
            send_message_text("<b>🚀 NEW COINS: </b>")
            for crypto in coins:
                message = textwrap.dedent(f"""
                    <b>🪙 {crypto.get("name")}</b>
                    <i>Contract:</i> {crypto.get("contract")}
                    <a href="{crypto.get("url")}">🔗 INFO</a>
                    <i>Created at:</i> {crypto.get("created_at")} ({crypto.get("minutes_since_creation")} min ago)
                    <i>FDV:</i> {crypto.get("fdv")}
                    <i>Volume:</i> {crypto.get("volume")}
                    <i>Price change:</i> {crypto.get("price_change_percentage")}%
                    <i>Transactions:</i> {crypto.get("transactions_buy")} (Buys) / {crypto.get("transactions_sell")} (Sells)
                    """).strip()
                send_message_text(message)
    else:
        send_message_text("<b>❌ No new cryptos were added. </b>")