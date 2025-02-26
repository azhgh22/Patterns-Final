from __future__ import annotations

from dataclasses import dataclass

from playground.core.services.classes.campaign_classes import (
    CampaignInterface,
    CampaignRequestWithType,
)


@dataclass
class Campaign:
    id: str
    description: CampaignRequestWithType

    def get_campaign(self) -> CampaignInterface:
        from playground.core.services.classes.campaign_factory import CampaignFactory

        return CampaignFactory.create_campaign(
            self.description.type, **self.description.params
        )

    def equals(self, second_campaign: Campaign) -> bool:
        return (
            self.description.type == second_campaign.description.type
            and self.description.params == second_campaign.description.params
        )
