from typing import Protocol

from playground.core.services.interfaces.memory.campaign_repository import CampaignRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import ICampaignService
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)


class IServiceChooser(Protocol):
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        pass

    def get_campaign_service(self, campaign_repo: CampaignRepository) -> ICampaignService:
        pass