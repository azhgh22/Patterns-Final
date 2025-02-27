from dataclasses import dataclass


@dataclass
class SalesItem:
    currency_id: str
    total_price: int
