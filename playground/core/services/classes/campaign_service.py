from dataclasses import dataclass
from typing import List
from uuid import uuid4

from playground.core.models.campaign import Campaign, CampaignRequestWithType
from playground.core.models.receipt import Receipt
from playground.core.services.classes.campaign_factory import CampaignRequestFactory, CampaignFactory
from playground.infra.memory.in_memory.campaign_in_memory_repository import CampaignInMemoryRepository
from playground.core.services.interfaces.memory.campaign_repository import CampaignRepository


@dataclass
class CampaignService:
    repo: CampaignRepository = CampaignInMemoryRepository()
    factory: CampaignRequestFactory = CampaignRequestFactory()

    def create(self, campaign: CampaignRequestWithType) -> Campaign:
        res = Campaign(id=str(uuid4()), description=campaign)
        self.repo.add_campaign(res)
        return res

    def apply(self, receipt: Receipt) -> Receipt:
        res = self.repo.apply_campaigns(receipt)
        return res

    def get_by_id(self, campaign_id: str) -> Campaign:
        return self.repo.get_by_id(campaign_id)

    def get_all(self) -> List[Campaign]:
        return self.repo.get_all()

    def get_campaign_request_with_type_instance(self, campaign_type: str, **kwargs) -> CampaignRequestWithType:
        return self.factory.create_campaign(campaign_type=campaign_type, **kwargs).to_request()

    def delete(self, campaign_id: str) -> Campaign:
        self.repo.delete_campaign(campaign_id)