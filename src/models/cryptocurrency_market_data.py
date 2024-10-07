from dataclasses import dataclass


@dataclass
class CryptocurrencyMarketData:
    id: str
    name: str
    creation_date: str  # cast to date
    chain: str
    initial_price: float
    current_price: float
    current_price_percentage: float
    higher_price: float
    higher_price_percentage: float
    higher_price_date: str  # cast to date
    lower_price: float
    lower_price_percentage: float
    lower_price_date: str  # cast to date
    price_change_percentage_24h: float
