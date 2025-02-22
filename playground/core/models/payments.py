from dataclasses import dataclass


@dataclass
class Payment:
    id: int
    receipt_id: int
    currency_id: int
    amount: int


@dataclass
class PaymentRequest:
    receipt_id: int
    currency_id: int
    amount: int
