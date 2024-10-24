from dataclasses import dataclass
from typing import List


@dataclass
class Cryptocurrency:
    id: str
    name: str
    price: float
    platform: str
    categories: List[str]
    description: str
    categories: List[str]
    homepage: str
    blockchain_sites: List[str]
    additional_notices: List[str]
    last_added: str
