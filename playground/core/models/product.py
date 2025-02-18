from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Product:
    id: str
    name: str
    barcode: str
    price: int


@dataclass
class ProductRequest(BaseModel):
    name: str
    barcode: str
    price: int


@dataclass
class ProductResponse(BaseModel):
    id: str
    name: str
    barcode: str
    price: int
