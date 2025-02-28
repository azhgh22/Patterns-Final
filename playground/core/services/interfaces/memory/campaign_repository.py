from typing import List, Protocol

from playground.core.models.campaign import Campaign


class CampaignRepository(Protocol):
    def add_campaign(self, campaign: Campaign) -> None:
        pass

    def get_by_id(self, campaign_id: str) -> Campaign:
        pass

    def get_all(self) -> List[Campaign]:
        pass

    def delete_campaign(self, campaign_id: str) -> None:
        pass
