from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List

from playground.core.models.receipt import Receipt


@dataclass
class CampaignRequestWithType:
    type: str
    params: dict[str, typing.Any]


class CampaignInterface(ABC):
    @abstractmethod
    def apply(self, receipt: Receipt) -> Receipt:
        pass

    @classmethod
    @abstractmethod
    def create(cls, **kwargs: Any) -> "CampaignInterface":  # Return type is CampaignInterface
        pass

    @abstractmethod
    def to_request(self) -> CampaignRequestWithType:
        pass


class BuyNGetNCampaign(CampaignInterface):
    def __init__(self, required_quantity: int, product_id: str) -> None:
        self.required_quantity = required_quantity
        self.product_id = product_id

    def apply(self, receipt: Receipt) -> Receipt:
        for item in receipt.products:
            if item.product_id == self.product_id and item.quantity >= self.required_quantity:
                item.quantity += item.quantity
        receipt.discounted_total = receipt.total
        return receipt

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(
            type="buy_n_get_n",
            params={
                "required_quantity": self.required_quantity,
                "product_id": self.product_id,
            },
        )

    @classmethod
    def create(cls, **kwargs: typing.Any) -> CampaignInterface:
        required_quantity = kwargs.get("required_quantity")
        product_id = kwargs.get("product_id")

        if not isinstance(required_quantity, int):
            raise TypeError("required_quantity must be an int")
        if not isinstance(product_id, str):
            raise TypeError("product_id must be a str")
        return cls(required_quantity, product_id)


class DiscountProductCampaign(CampaignInterface):
    def __init__(self, discount_percentage: float, applicable_product: str) -> None:
        self.applicable_product = applicable_product
        self.discount_percentage = discount_percentage

    def apply(self, receipt: Receipt) -> Receipt:
        new_total = 0
        receipt.discounted_total = receipt.total
        applied = False
        for item in receipt.products:
            if item.product_id == self.applicable_product:
                item.total = round(item.total * (1 - self.discount_percentage / 100))
                applied = True
            new_total += item.total
        if applied:
            receipt.discounted_total = new_total
        return receipt

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(
            type="discount_product",
            params={
                "discount_percentage": self.discount_percentage,
                "applicable_product": self.applicable_product,
            },
        )

    @classmethod
    def create(cls, **kwargs: typing.Any) -> CampaignInterface:
        discount_percentage = kwargs.get("discount_percentage")
        applicable_product = kwargs.get("applicable_product")
        if not isinstance(discount_percentage, (int, float)):
            raise TypeError("discount_percentage must be a float")
        if not isinstance(applicable_product, str):
            raise TypeError("product_id must be a str")
        return cls(discount_percentage, applicable_product)


class DiscountReceiptCampaign(CampaignInterface):
    def __init__(
        self, discount_percentage: float, applicable_receipt: str, required_price: int
    ) -> None:
        self.applicable_receipt = applicable_receipt
        self.discount_percentage = discount_percentage
        self.required_price = required_price

    def apply(self, receipt: Receipt) -> Receipt:
        receipt.discounted_total = receipt.total
        if receipt.total >= self.required_price:
            receipt.discounted_total = round(
                receipt.total * (1 - self.discount_percentage / 100)
            )
        return receipt

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(
            type="discount_receipt",
            params={
                "discount_percentage": self.discount_percentage,
                "applicable_receipt": self.applicable_receipt,
                "required_price": self.required_price,
            },
        )

    @classmethod
    def create(cls, **kwargs: typing.Any) -> CampaignInterface:
        discount_percentage = kwargs.get("discount_percentage")
        applicable_receipt = kwargs.get("applicable_receipt")
        required_price = kwargs.get("required_price")
        if not isinstance(discount_percentage, (int, float)):
            raise TypeError("discount_percentage must be a float")
        if not isinstance(applicable_receipt, str):
            raise TypeError("product_id must be a str")
        if not isinstance(required_price, int):
            raise TypeError("product_id must be a str")
        return cls(discount_percentage, applicable_receipt, required_price)


class ComboCampaign(CampaignInterface):
    def __init__(self, product_ids: List[str], discount_percentage: float) -> None:
        if product_ids is None:
            product_ids = []
        self.product_ids = product_ids
        self.discount_percentage = discount_percentage

    def apply(self, receipt: Receipt) -> Receipt:
        receipt.discounted_total = receipt.total
        if all(
            any(item.product_id == pid for item in receipt.products) for pid in self.product_ids
        ):
            new_total = 0
            for item in receipt.products:
                if item.product_id in self.product_ids:
                    item.total = round(item.total * (1 - self.discount_percentage / 100))
                new_total += item.total
            receipt.discounted_total = new_total
        return receipt

    @classmethod
    def create(cls, **kwargs: typing.Any) -> CampaignInterface:
        product_ids = kwargs.get("product_ids")
        discount_percentage = kwargs.get("discount_percentage")
        if not isinstance(product_ids, list) or not all(isinstance(p, str) for p in product_ids):
            raise TypeError("product_ids must be a list of strings")
        if not isinstance(discount_percentage, (int, float)):
            raise TypeError("discount_percentage must be a float")
        return cls(product_ids, discount_percentage)

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(
            type="combo",
            params={
                "product_ids": self.product_ids,
                "discount_percentage": self.discount_percentage,
            },
        )
