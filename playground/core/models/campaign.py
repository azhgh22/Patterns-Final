from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any

from playground.core.services.classes.campaign_classes import CampaignInterface


@dataclass
class Campaign:
    id: str
    description: CampaignRequestWithType

    def get_campaign(self) -> CampaignInterface:
        from playground.core.services.classes.campaign_factory import CampaignFactory
        return CampaignFactory.create_campaign(self.description.type, **self.description.params)

@dataclass
class CampaignRequestWithType:
    type: str
    params: dict[str, Any]


class CampaignRequestInterface(ABC):
    @staticmethod
    @abstractmethod
    def create(**kwargs) -> CampaignRequestInterface:
        pass

    @abstractmethod
    def to_request(self) -> CampaignRequestWithType:
        pass


class BuyNGetNCampaignRequest(CampaignRequestInterface):
    def __init__(self, required_quantity: int, free_quantity: int, product_id: int, description: str):
        self.required_quantity = required_quantity
        self.free_quantity = free_quantity
        self.product_id = product_id
        self.description = description

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(type="buy_n_get_n", params={"required_quantity": self.required_quantity,
                                                                    "free_quantity": self.free_quantity,
                                                                    "product_id": self.product_id,
                                                                    "description": self.description,})

    @classmethod
    def create(cls, required_quantity: int, free_quantity: int, product_id: int, description: str):
        return cls(required_quantity, free_quantity, product_id, description)



class DiscountCampaignRequest(CampaignRequestInterface):
    def __init__(self, discount_percentage: float, applicable_products: List[int], description: str):
        self.discount_percentage = discount_percentage
        self.applicable_products = applicable_products
        self.description = description

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(type="discount", params={"discount_percentage": self.discount_percentage,
                                                                "applicable_products": self.applicable_products,
                                                                "description": self.description,})

    @classmethod
    def create(cls, discount_percentage: float, applicable_products: List[int], description: str):
        return cls(discount_percentage, applicable_products, description)




class ComboCampaignRequest(CampaignRequestInterface):
    def __init__(self, product_ids: List[int], combo_price: float, description: str):
        self.product_ids = product_ids
        self.combo_price = combo_price
        self.description = description

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(type="combo", params={"product_ids": self.product_ids,
                                                            "combo_price": self.combo_price,
                                                            "description": self.description,})

    @classmethod
    def create(cls, product_ids: List[int], combo_price: float, description: str):
        return cls(product_ids, combo_price, description)

