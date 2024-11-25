from src.utils.telegram_utils import send_message_text


def send_last_half_hour_coins_message(coins):
    if len(coins) > 0:
        send_message_text("<b>🚀 NEW COINS: </b>")
        for crypto in coins:
            message = f"""
                <b>🪙 {crypto.name}</b>
                <i>Platform:</i> {crypto.platform}
                <i>Contract:</i> {crypto.contract}
                <i>Price:</i> ${crypto.price}
                <i>Categories:</i> {", ".join(crypto.categories)}
                <i>Description:</i> {crypto.description}
                <a href="{crypto.homepage}">🔗 Homepage</a>
                <i>Last added:</i> {crypto.last_added}
                """
            send_message_text(message)
    else:
        send_message_text("<b>❌ No new cryptos were added. </b>")