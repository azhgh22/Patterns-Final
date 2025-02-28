from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    barcode: str
    price: int

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.barcode == other.barcode
            and self.price == other.price
        )


@dataclass
class ProductRequest:
    name: str
    barcode: str
    price: int


@dataclass
class ProductReport:
    id: str
    quantity: int

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, type(self)):
            return False
        return self.id == other.id and self.quantity == other.quantity
