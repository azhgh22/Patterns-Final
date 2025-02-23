from dataclasses import dataclass


@dataclass
class Payment:
    receipt_id: str
    currency_id: str
    amount: int

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return (
            self.receipt_id == other.receipt_id
            and self.currency_id == other.currency_id
            and self.amount == other.amount
        )


@dataclass
class PaymentRequest:
    receipt_id: str
    currency_id: str
