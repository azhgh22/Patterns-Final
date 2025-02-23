from dataclasses import dataclass


@dataclass
class Payment:
    receipt_id: str
    currency_id: str
    amount: int


@dataclass
class PaymentRequest:
    receipt_id: str
    currency_id: str
