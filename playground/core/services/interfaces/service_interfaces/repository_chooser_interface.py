from typing import Protocol

from playground.core.services.interfaces.memory.campaign_repository import CampaignRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)


class IRepositoryChooser(Protocol):
    def get_product_repo(self) -> ProductRepository:
        pass

    def get_campaign_repo(self) -> CampaignRepository:
        pass
