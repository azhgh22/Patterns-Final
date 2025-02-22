from playground.core.services.interfaces.memory.campaign_repository import (
    CampaignRepository,
)
from playground.core.services.interfaces.memory.product_repository import (
    ProductRepository,
)
from playground.infra.memory.in_memory.campaign_in_memory_repository import (
    CampaignInMemoryRepository,
)
from playground.infra.memory.in_memory.products_in_memory_repository import (
    ProductInMemoryRepository,
)


class InMemoryChooser:
    def __init__(
        self,
        product_repo: ProductRepository = ProductInMemoryRepository(),
        campaign_repo: CampaignRepository = CampaignInMemoryRepository(),
    ) -> None:
        self.product_repository = product_repo
        self.campaign_repository = campaign_repo

    def get_product_repo(self) -> ProductRepository:
        return self.product_repository

    def get_campaign_repo(self) -> CampaignRepository:
        return self.campaign_repository
