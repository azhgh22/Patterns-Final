from __future__ import annotations

from playground.core.models.receipt import Receipt


from abc import ABC, abstractmethod
from typing import List
from playground.core.models.receipt import ReceiptResponse

class CampaignInterface(ABC):

    @abstractmethod
    def apply(self, receipt: Receipt) -> Receipt:
        pass

    @staticmethod
    @abstractmethod
    def create(**kwargs) -> CampaignInterface:
        pass


class BuyNGetNCampaign(CampaignInterface):
    def __init__(self, required_quantity: int = 1, product_id: str = "1") -> None:
        self.required_quantity = required_quantity
        self.product_id = product_id

    def apply(self, receipt: Receipt) -> Receipt:
        for item in receipt.products:
            if item.id == self.product_id and item.quantity >= self.required_quantity:
                item.quantity += self.required_quantity
        return receipt

    @staticmethod
    def create(required_quantity: int = 1, product_id: str = "1") -> BuyNGetNCampaign:
        return BuyNGetNCampaign(required_quantity, product_id)


class DiscountCampaign(CampaignInterface):
    def __init__(self, discount_percentage: float = 50, product_id: str="1") -> None:
        self.product_id = product_id
        self.discount_percentage = discount_percentage

    def apply(self, receipt: Receipt) -> Receipt:
        for item in receipt.products:
            if item.id == self.product_id:
                item.price *= (1 - self.discount_percentage / 100)
        return receipt

    @staticmethod
    def create(discount_percentage: float =50, product_id: str="1") -> DiscountCampaign:
        return DiscountCampaign(discount_percentage, product_id)


class ComboCampaign(CampaignInterface):
    def __init__(self, product_ids=None, discount_percentage: float = 50) -> None:
        if product_ids is None:
            product_ids = []
        self.product_ids = product_ids
        self.discount_percentage = discount_percentage

    def apply(self, receipt: Receipt) -> Receipt:
        if all(any(item.id == pid for item in receipt.products) for pid in self.product_ids):
            for item in receipt.products:
                if item.id in self.product_ids:
                    item.price *= (1 - self.discount_percentage / 100)
        return receipt

    @staticmethod
    def create(product_ids=None, discount_percentage: float = 50) -> ComboCampaign:
        if product_ids is None:
            product_ids = []
        return ComboCampaign(product_ids, discount_percentage)

