import copy
import typing
from dataclasses import dataclass
from typing import List
from uuid import uuid4

from playground.core.models.campaign import Campaign
from playground.core.models.receipt import Receipt
from playground.core.services.classes.campaign_classes import (
    CampaignRequestWithType,
)
from playground.core.services.classes.campaign_factory import (
    CampaignFactory,
)
from playground.core.services.interfaces.memory.campaign_repository import (
    CampaignRepository,
)
from playground.infra.memory.in_memory.campaign_in_memory_repository import (
    CampaignInMemoryRepository,
)


@dataclass
class CampaignService:
    repo: CampaignRepository = CampaignInMemoryRepository()
    factory: CampaignFactory = CampaignFactory()

    def create(self, campaign: CampaignRequestWithType) -> Campaign:
        res = Campaign(id=str(uuid4()), description=campaign)
        self.repo.add_campaign(res)
        return res

    def apply(self, receipt: Receipt) -> Receipt:
        campaigns = self.get_all()

        res = copy.deepcopy(receipt)
        discounted = copy.deepcopy(receipt)
        discounted.discounted_total = discounted.total
        for campaign in campaigns:
            if campaign.description.type != "buy_n_get_n":
                tmp = campaign.get_campaign().apply(res)

                if (
                    tmp.discounted_total is not None
                    and tmp.discounted_total < discounted.discounted_total
                ):
                    discounted = tmp
            else:
                discounted = campaign.get_campaign().apply(discounted)
                res = campaign.get_campaign().apply(res)
        return discounted

    def get_by_id(self, campaign_id: str) -> Campaign:
        return self.repo.get_by_id(campaign_id)

    def get_all(self) -> List[Campaign]:
        return self.repo.get_all()

    def get_campaign_request_with_type_instance(
        self, campaign_type: str, **kwargs: typing.Any
    ) -> CampaignRequestWithType:
        return self.factory.create_campaign(campaign_type=campaign_type, **kwargs).to_request()

    def delete(self, campaign_id: str) -> None:
        self.repo.delete_campaign(campaign_id)
