from typing import Protocol


class ICurrencyConverter(Protocol):
    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        pass
