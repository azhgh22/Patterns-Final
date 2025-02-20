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
    def __init__(self, required_quantity: int = 1, product_id: str = "1"):
        self.required_quantity = required_quantity
        self.product_id = product_id

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(type="buy_n_get_n", params={"required_quantity": self.required_quantity,
                                                                    "product_id": self.product_id,
                                                                    })

    @classmethod
    def create(cls, required_quantity: int = 1, product_id: str = "1"):
        return cls(required_quantity, product_id)



class DiscountCampaignRequest(CampaignRequestInterface):
    def __init__(self, discount_percentage: float = 50, applicable_product: str="1"):
        self.applicable_product = applicable_product
        self.discount_percentage = discount_percentage

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(type="discount", params={"discount_percentage": self.discount_percentage,
                                                                "applicable_product": self.applicable_product,
                                                                })

    @classmethod
    def create(cls, discount_percentage: float = 50, applicable_product: str = "1"):
        return cls(discount_percentage, applicable_product)




class ComboCampaignRequest(CampaignRequestInterface):
    def __init__(self, product_ids: List[str]=None, discount_percentage: float = 50):
        if product_ids is None:
            product_ids = []
        self.product_ids = product_ids
        self.discount_percentage = discount_percentage

    def to_request(self) -> CampaignRequestWithType:
        return CampaignRequestWithType(type="combo", params={"product_ids": self.product_ids,
                                                            "discount_percentage": self.discount_percentage,
                                                            })

    @classmethod
    def create(cls, product_ids: List[str] = None, discount_percentage: float = 50):
        return cls(product_ids, discount_percentage)

