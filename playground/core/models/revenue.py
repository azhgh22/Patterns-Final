from dataclasses import dataclass


@dataclass
class Revenue:
    amount: float
    currency_id: str

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return self.amount == other.amount and self.currency_id == other.currency_id
