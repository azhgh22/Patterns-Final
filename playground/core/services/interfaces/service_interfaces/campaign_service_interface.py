from typing import Protocol, List

from playground.core.models.campaign import Campaign, CampaignRequestInterface, CampaignRequestWithType
from playground.core.models.receipt import Receipt


class ICampaignService(Protocol):
    def create(self, campaign: CampaignRequestWithType) -> Campaign:
        pass

    def apply(self, receipt: Receipt) -> Receipt:
        pass

    def get_by_id(self, campaign_id: str) -> Campaign:
        pass

    def get_all(self) -> List[Campaign]:
        pass

    def get_campaign_request_with_type_instance(self, campaign_type: str, **kwargs) -> CampaignRequestWithType:
        pass

    def delete(self, campaign_id: str) -> None:
        pass