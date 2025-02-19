from playground.core.services.classes.campaign_service import CampaignService
from playground.core.services.classes.product_service import ProductService
from playground.core.services.interfaces.memory.campaign_repository import CampaignRepository
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.core.services.interfaces.service_interfaces.campaign_service_interface import ICampaignService
from playground.core.services.interfaces.service_interfaces.product_service_interface import (
    IProductService,
)


class ServiceChooser:
    def get_product_service(self, product_repo: ProductRepository) -> IProductService:
        return ProductService(product_repo)

    def get_campaign_service(self, campaign_repo: CampaignRepository) -> ICampaignService:
        return CampaignService(campaign_repo)
