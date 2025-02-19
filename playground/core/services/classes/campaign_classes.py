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
    def __init__(self, required_quantity: int, free_quantity: int, product_id: int) -> None:
        self.required_quantity = required_quantity
        self.free_quantity = free_quantity
        self.product_id = product_id

    def apply(self, receipt: Receipt) -> Receipt:
        for item in receipt.products:
            if item.id == self.product_id and item.quantity >= self.required_quantity:
                item.quantity += self.free_quantity
        return receipt

    @staticmethod
    def create(required_quantity: int, free_quantity: int, product_id: int) -> BuyNGetNCampaign:
        return BuyNGetNCampaign(required_quantity, free_quantity, product_id)


class DiscountCampaign(CampaignInterface):
    def __init__(self, product_id: int, discount_percentage: float) -> None:
        self.product_id = product_id
        self.discount_percentage = discount_percentage

    def apply(self, receipt: Receipt) -> Receipt:
        for item in receipt.products:
            if item.id == self.product_id:
                item.price *= (1 - self.discount_percentage / 100)
        return receipt

    @staticmethod
    def create(product_id: int, discount_percentage: float) -> DiscountCampaign:
        return DiscountCampaign(product_id, discount_percentage)


class ComboCampaign(CampaignInterface):
    def __init__(self, product_ids: List[int], discount_percentage: float) -> None:
        self.product_ids = product_ids
        self.discount_percentage = discount_percentage

    def apply(self, receipt: Receipt) -> Receipt:
        if all(any(item.id == pid for item in receipt.products) for pid in self.product_ids):
            for item in receipt.products:
                if item.id in self.product_ids:
                    item.price *= (1 - self.discount_percentage / 100)
        return receipt

    @staticmethod
    def create(product_ids: List[int], discount_percentage: float) -> ComboCampaign:
        return ComboCampaign(product_ids, discount_percentage)

