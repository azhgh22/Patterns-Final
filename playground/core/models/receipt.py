from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from playground.core.models.product import ProductResponse, Product


@dataclass
class Receipt:
    id: str
    status: str
    products: List[Product]


@dataclass
class ReceiptRequest(BaseModel):
    status: str


@dataclass
class ReceiptResponse(BaseModel):
    id: str
    status: str
    products: List[ProductResponse]
    total: int


@dataclass
class AddProductRequest(BaseModel):
    id: str
    quantity: int